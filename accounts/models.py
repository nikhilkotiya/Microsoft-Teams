from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,AbstractUser
from .manager import MyAccountManager
from django.contrib.auth.models import PermissionsMixin
class User(AbstractUser):
    username= models.CharField(unique=False,null=True,blank=True,max_length=20)
    email = models.EmailField(unique = True, verbose_name='email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyAccountManager()
    def __str__(self):
        return self.email