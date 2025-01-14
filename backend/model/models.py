import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "User")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(max_length=15, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        ordering = ["-id"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Model(models.Model):
    model_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="models"
    )
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    height = models.PositiveIntegerField()

    HAIR_CHOICES = [
        ("blonde", "Blonde"),
        ("brown", "Brown"),
        ("black", "Black"),
        ("red", "Red"),
        ("grey", "Gray"),
        ("other", "Other"),
    ]
    hair = models.CharField(max_length=20, choices=HAIR_CHOICES)

    EYE_COLOR_CHOICES = [
        ("blue", "Blue"),
        ("green", "Green"),
        ("brown", "Brown"),
        ("gray", "Gray"),
        ("hazel", "Hazel"),
    ]
    eye_color = models.CharField(max_length=10, choices=EYE_COLOR_CHOICES)

    shoe_size = models.FloatField()
    bust = models.PositiveIntegerField()
    waist = models.PositiveIntegerField()
    hips = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


def model_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(instance.model.user.first_name)}"
        f"-{slugify(instance.model.user.last_name)}"
        f"-{uuid.uuid4()}.{extension}"
    )
    return os.path.join(
        "uploads",
        "models",
        f"{slugify(instance.model.user.first_name)}"
        f"-{slugify(instance.model.user.last_name)}",
        filename
    )


class ModelImages(models.Model):
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=model_image_file_path)
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.model.full_name}: {self.image.name}"
