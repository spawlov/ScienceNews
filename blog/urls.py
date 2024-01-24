from django.urls import path

from .views import (
    ContactsView,
    HomeView,
    PostDetailView,
    PostsByCategoryView,
    PostsByTagView,
    PostsListView,
    SearchView,
    add_subscriber,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("posts/", PostsListView.as_view(), name="posts"),
    path("search/", SearchView.as_view(), name="search"),
    path("subscribe/", add_subscriber, name="subscribe"),
    path("post/<str:slug>/", PostDetailView.as_view(), name="post"),
    path(
        "category/<str:slug>/",
        PostsByCategoryView.as_view(),
        name="category",
    ),
    path("tag/<str:slug>/", PostsByTagView.as_view(), name="tag"),
]
