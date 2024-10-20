from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin
)

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self.save_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.save_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("Librarian", "Librarian"),
        ("Office Staff", "Office Staff"),   
    ]

    first_name = models.CharField(
        max_length=50,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    phone_number = models.CharField(
        max_length=15, 
        verbose_name='Phone'
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,  
        verbose_name="Role"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        return self.first_name