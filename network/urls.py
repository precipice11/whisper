
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit/", views.submitPost, name='submitPost'),
    path("<int:user_id>/", views.profileView, name='profile'),
    path("follow/<int:user_id>/", views.follow_user, name="follow"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow"),
    path("following/", views.followingPage, name="following"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),

]

