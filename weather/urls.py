from django.urls import path

from . import views

app_name = "weather"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/", views.profile_page, name="profile_page"),
    path("friend_request", views.friend_request, name="friend_request"),
    path("friend_list", views.friend_list, name="friend_list"),


    # API Routes
    path("create_post", views.compose, name="compose"),
    path("add_friend", views.add_friend, name="add_friend"),
    path("accept_friend", views.accept_friend, name="accept_friend"),
    path("load_posts", views.load_posts, name="load_posts"),



]