from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Permission
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,mobile,firstname,lastname,password=None):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,mobile=mobile,firstname=firstname,lastname=lastname)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,username,mobile,firstname,lastname,password=None):
        user = self.create_user(email,username,mobile,firstname,lastname,password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_permissions' 
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    mobile = PhoneNumberField(unique=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    uid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','mobile','firstname','lastname']

    def __str__(self):
        return self.username