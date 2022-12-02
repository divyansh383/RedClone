from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        extra_fields.setdefault('profile_picture', "default/static")
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
        
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name']

    def get_full_name(self):
        return self.first_name+" "+self.last_name
    def get_short_name(self):
        return self.first_name
    def __str__(self):
        return self.email