from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # access a users posts with user.posts.all()
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )


class Post(models.Model):
    # id already exists.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    postContent = models.CharField(max_length=500)
    dateCreated = models.DateTimeField(auto_now_add=True)
    # comments -> user's
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()


# Add additional models to represent posts, likes, followers.

# remember to run python3 manage.py makemigrations and python3 manage.py migrate.