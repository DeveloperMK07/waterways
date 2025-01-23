from django.urls import path
from . import views
from .views import add_article

urlpatterns = [
    path('', views.home, name='home'),
    # Add other URL patterns here
    path('add-article/', add_article, name='add_article'),
]
