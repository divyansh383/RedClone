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
        extra_fields.setdefault('is_verified', True)
        
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
    profile_picture=models.ImageField(blank=True,upload_to='profiles',default="default.jpg")
    folowers=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','is_verified','profile_picture']

    def get_full_name(self):
        return self.first_name+" "+self.last_name
    def get_short_name(self):
        return self.first_name
    def __str__(self):
        return self.email

class Post(models.Model):
    poster=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    file=models.FileField(blank=True,upload_to='posts',default='default.png')
    caption=models.TextField(max_length=255,null=True,blank=True,default=None)
    likes=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
    def __str__(self):
        return self.poster.first_name+"_post_"+str(self.id)

class Comment(models.Model):
    comment_post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',null=True, related_name='replies', on_delete=models.CASCADE,default=None)
    text=models.TextField(max_length=255)
    commented_on=models.DateTimeField(auto_now_add=True)
    commented_by=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)+"_on_"+str(self.comment_post.id)+"_by_"+str(self.commented_by.id)

class LikedPost(models.Model):
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    liked_post=models.ForeignKey(Post,on_delete=models.CASCADE,null=False)
    liked_on=models.DateTimeField(auto_now_add=True)
    value=models.IntegerField(default=0)
    class Meta:
        unique_together = ('liked_by', 'liked_post')
    def __str__(self):
        return str(self.liked_by)+"|" + str(self.liked_post) +"|" +str(self.liked_post.likes)