from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, first_name, last_name, phone, password):
        user = self.model(
            username=username,
            email=self.normalize_eemail(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, first_name, last_name, phone, password):
        user = self.create_user(
            username,
            email=self.normalize_eemail(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password):
        user = self.create_user(
            username,
            email=self.normalize_eemail(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(
        max_length=100,
        verbose_name='',
    )
    password = models.CharField(
        max_length=100,
        verbose_name='',
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='',
    )
    middle_name = models.CharField(
        max_length=100,
        verbose_name='',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='',
    )
    email = models.EemailField(
        max_length=254,
        verbose_name='',
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='',
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'email', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.username
