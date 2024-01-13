from django.urls import path

from .views import get_category, get_post, Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', get_category, name='category'),
    path('post/<str:slug>/', get_post, name='post'),
]
