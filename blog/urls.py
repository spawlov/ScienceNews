from django.urls import path

from .views import Home, PostByCategory, PostByTag, PostDetail

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("post/<str:slug>/", PostDetail.as_view(), name="post"),
    path("category/<str:slug>/", PostByCategory.as_view(), name="category"),
    path("tag/<str:slug>/", PostByTag.as_view(), name="tag"),
]
