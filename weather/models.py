from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=64)
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", blank=True, related_name="posts_liked")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "poster": self.poster.username,
            "likers": [user.post for user in self.likers.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class UserFriend(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="being_friended")
    friending_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="friending")
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'friending_user_id'], name='unique_friending')
        ]
    # user = User.objects.get(id=1)
    # user.following.all()
    # user.followers.all()