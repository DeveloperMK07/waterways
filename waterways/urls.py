from django.contrib import admin
from django.urls import path
from main import views  # Import all views from the main app
from django.conf import settings
from django.conf.urls.static import static

# Import specific views at the top of the file
from main.views import delete_user, upvote_article, article_detail, delete_article

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Homepage URL
    path('articles/', views.articles, name='articles'),  # Articles URL
    path('agriculture/', views.agriculture, name='agriculture'),  # Agriculture URL
    path('join/', views.join, name='join'),  # Join Us URL
    
    # User authentication paths
    path('login/', views.login_view, name='login'),  # Login URL
    path('register/', views.register, name='register'),  # Register URL
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    
    # Article-specific paths
    path('add-article/', views.add_article, name='add_article'),  # Add Article URL

    # Create a separate URL pattern for your custom admin views
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin Dashboard
    path('custom-admin/manage-users/', views.manage_users, name='manage_users'),  # Manage Users
    path('custom-admin/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),  # Edit User
    path('admin/delete-user/<int:user_id>/', delete_user, name='delete_user'),  # Delete User
    path('article/upvote/<int:article_id>/', upvote_article, name='upvote_article'),  # Upvote Article
    path('article/delete/<int:article_id>/', delete_article, name='delete_article'),  # Delete Article

    path('article/<int:article_id>/', article_detail, name='article_detail'),  # Article Detail

    path('manage-events/', views.manage_events, name='manage_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
