from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .manager import MyAccountManager
from django.contrib.auth.models import PermissionsMixin
is_active = (
    ('True', 'True'),
    ('False', 'False')
)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True, blank=False ,verbose_name='first_name')
    email = models.EmailField(null=True, blank=False,unique = True, verbose_name='email')
    last_name = models.CharField(max_length=20,null=True, blank=False,verbose_name='last_name')
    password = models.CharField(max_length=20,null=True,blank=False,verbose_name='password')
    username = models.CharField(max_length=20,verbose_name='username')
    date_joined = models.DateTimeField(verbose_name = "date joined" ,auto_now_add=True )
    last_login = models.DateTimeField(verbose_name= 'last login',null=True,blank=True,auto_now=True) 
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = MyAccountManager()
    def __str__(self):
        return self.email
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    def has_perm(self, perm ,obj=None):
        return self.is_admin
    def has_module_perms(self,app_Label):
        return True

# video test done