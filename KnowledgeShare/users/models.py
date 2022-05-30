from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField('profile_images', null=True,
                                      blank=True, upload_to='profile_images')
    bio = models.TextField(max_length=500, blank=True)
    followers = models.ManyToManyField('self',
                                       blank=True,
                                       related_name='user_followers',
                                       symmetrical=False)
    following = models.ManyToManyField('self',
                                       blank=True,
                                       related_name='user_following',
                                       symmetrical=False)

    def count_followers(self) -> int:
        return self.followers.count()

    def count_following(self) -> int:
        return self.following.count()
