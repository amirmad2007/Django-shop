from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


# you can add managers in managers.py
class MyUserManager(BaseUserManager):
    def create_user(self, email,username,phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
     
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            phone_number = phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,password ,username , phone_number ,  email = None ,):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email = email,
            password=password,
            username = username,
            phone_number= phone_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        blank= True,
        null= True,
        unique=True,
    )
    username = models.CharField( max_length=50, unique= True)
    date_of_birth = models.DateField(null=True , blank= True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField( upload_to="profile_Pictures", blank=True , null=True)
    phone_number =models.CharField(max_length=12,unique=True)
    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True




class OTP(models.Model):

    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=4)   # مثلاً 6 رقم
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)
        
    def is_valid(self):
        """بررسی اینکه OTP منقضی نشده و استفاده نشده"""
        return  timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
