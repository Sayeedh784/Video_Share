from distutils.command.upload import upload
from email.mime import image
from hashlib import blake2b
from venv import create
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from .validators import file_size
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, email, name,password=None,password2=None):
      """
      Creates and saves a User with the given email,name,tc and password.
      """
      if not email:
          raise ValueError('Users must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name = name,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, password=None):
      """
      Creates and saves a superuser with the given email, date of
      birth and password.
      """
      user = self.create_user(
        email,
        password=password,
        name=name,
        
      )
      user.is_admin = True
      user.save(using=self._db)
      return user
class User(AbstractBaseUser):
  email = models.EmailField(verbose_name='Email',max_length=255,unique=True)
  name = models.CharField(max_length=50)
  location = models.CharField(max_length=100,blank=True,null=True)
  image= models.ImageField(upload_to="images",blank=True,null=True)
  is_active=models.BooleanField(default=True)
  is_admin=models.BooleanField(default=False)

  def get_absolute_url(self):
    return reverse('profile', args=[str(self.id)])

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name',]

  def __str__(self):
    return self.email

  def has_perm(self,perm,obj=None):
    "Does the user have a specific permission?"
    #simplest possible answer: Yes,always
    return self.is_admin

  def has_module_perms(self,app_label):
    "Does the user have a specific permissions to view app `app_label`?"
    #simplest possible answer: Yes,always
    return True
  @property
  def is_staff(self):
    "Is the user a member of staff?"
    #simplest possible answer : All admins are staff
    return self.is_admin

class PostVideo(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  caption=models.CharField(max_length=100)
  video=models.FileField(upload_to="videos",validators=[file_size])
  description = models.TextField(max_length=255)
  publish_at = models.DateTimeField(auto_now_add=True)
  likes = models.ManyToManyField(User, blank=True, related_name='likes')
  dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

  def __str__(self):
    return self.caption

  def get_absolute_url(self):
    return reverse('profile', args=[str(self.id)])

