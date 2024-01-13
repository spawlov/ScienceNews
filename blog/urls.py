from django.urls import path

from .views import index, get_category

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:slug>/', get_category, name='category'),
]
