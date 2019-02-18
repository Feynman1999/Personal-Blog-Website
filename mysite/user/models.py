from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, verbose_name="昵称")

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)