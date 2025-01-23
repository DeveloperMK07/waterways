from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Article
import joblib
import pandas as pd



# Load your model and label encoders
model = joblib.load('main/ml_models/model.pkl')
label_encoders = {
    'State': joblib.load('main/ml_models/State_encoder.pkl'),
    'Soil Type': joblib.load('main/ml_models/Soil Type_encoder.pkl'),
    'Crop Type': joblib.load('main/ml_models/Crop Type_encoder.pkl')
}

# Home view
def home(request):
    return render(request, 'home.html')

# Articles list view
def articles(request):
    articles_list = Article.objects.all()  # Fetch all articles from the database
    return render(request, 'articles.html', {'articles': articles_list})  # Pass articles to the template

# Agriculture page view with machine learning model
def agriculture(request):
    recommendations = []
    if request.method == 'POST':
        state = request.POST['state']
        soil_type = request.POST['soil_type']
        crop_type = request.POST['crop_type']

        # Check if the inputs are valid
        if state not in label_encoders['State'].classes_:
            recommendations.append("Unknown state. Please provide a valid state.")
        elif soil_type not in label_encoders['Soil Type'].classes_:
            recommendations.append("Unknown soil type. Please provide a valid soil type.")
        elif crop_type not in label_encoders['Crop Type'].classes_:
            recommendations.append("Unknown crop type. Please provide a valid crop type.")
        else:
            # Convert inputs to numerical form using label encoders
            state_encoded = label_encoders['State'].transform([state])[0]
            soil_type_encoded = label_encoders['Soil Type'].transform([soil_type])[0]
            crop_type_encoded = label_encoders['Crop Type'].transform([crop_type])[0]

            # Create a DataFrame for the prediction input
            input_df = pd.DataFrame([[state_encoded, soil_type_encoded, crop_type_encoded]], 
                                    columns=['State', 'Soil Type', 'Crop Type'])

            # Predict conservation technique
            prediction = model.predict(input_df)
            recommendations.append(prediction[0])  # Store the prediction result

    return render(request, 'agriculture.html', {'recommendations': recommendations})
# In views.py
# from django.shortcuts import render

def join(request):
    return render(request, 'join.html')  # Ensure 'join.html' exists in the templates folder

# User Registration View
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        # Check if the email is already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used.")
            return render(request, 'register.html')

        # Create the user if everything is valid
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log the user in after successful registration
        login(request, user)

        # Redirect to login page
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                # Redirect to admin dashboard if user is admin
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')  # Redirect to home for regular users
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')  # Redirect to home after logout

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Manage Users View
@login_required
def manage_users(request):
    users = User.objects.all()  # Get all users
    return render(request, 'manage_users.html', {'users': users})

# Edit User View
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_superuser = 'is_admin' in request.POST  # Check if the admin checkbox is checked
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')
    return render(request, 'edit_user.html', {'user': user})

# Add article view
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        image = request.FILES.get('image')  # Handle optional image

        # Save the article to the database
        article = Article(title=title, content=content, category=category, image=image, author=request.user)
        article.save()

        # Display success message
        messages.success(request, 'Your article has been successfully submitted!')
        return redirect('articles')  # Redirect to articles page after saving

    return render(request, 'add_article.html')

# Delete User View
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get the user by ID
    if request.method == 'POST':
        user.delete()  # Delete the user
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')  # Redirect to the manage users page
    return render(request, 'confirm_delete_user.html', {'user': user})  # Render confirmation template

# Upvote Article View
@login_required
def upvote_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.upvotes += 1  # Increment the upvote count
    article.save()  # Save the changes
    messages.success(request, 'You have upvoted the article successfully!')
    return redirect('articles')  # Redirect to the articles page

# Article Detail View
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Retrieve the article
    return render(request, 'article_detail.html', {'article': article})  # Render the detail template

# Delete Article View
@user_passes_test(lambda u: u.is_superuser)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('articles')  # Redirect to the articles page after deletion
    
    return render(request, 'confirm_delete.html', {'article': article})

#new
from .models import Event
from django.shortcuts import render, redirect
from django.contrib import messages

# View to manage events
@login_required
def manage_events(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'admin/manage_events.html', {'events': events})

# Add Event View
@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        event = Event(title=title, description=description, start_date=start_date, end_date=end_date)
        event.save()

        messages.success(request, 'Event added successfully!')
        return redirect('manage_events')  # Redirect to manage events page

    return render(request, 'admin/add_event.html')

# Delete Event View
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('manage_events')

    return render(request, 'admin/confirm_delete_event.html', {'event': event})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NewsletterSubscriber  # Assuming you have a model for storing email addresses

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Save the email to the database (or handle accordingly)
        NewsletterSubscriber.objects.create(email=email)
        return HttpResponse("Thank you for subscribing!")  # Redirect or send confirmation
    return redirect('home')  # If it's a GET request, redirect to the homepage

from .models import NewsletterSubscriber
