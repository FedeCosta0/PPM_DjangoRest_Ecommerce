from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models

from utils.model_abstracts import Model


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name="",
            last_name=""
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, Model):
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserAddress(Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='user_address')
    address = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    postal_code = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=20, null=False)
    telephone = models.CharField(max_length=20)
