from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    #与User模型形成一对一关系，on_detele是删除关联和与之关联的数据，related_name
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    style = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


