from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required and must be set")

        email = self.normalize_email(email).strip().lower()
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        if not username:
            raise ValueError("Natural key (username/email) must be provided")
        return self.get(email__iexact=username)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name="Email",
    )

    first_name = models.CharField(
        max_length=64,
        verbose_name="Meno",
    )

    last_name = models.CharField(
        max_length=64,
        verbose_name="Priezvisko",
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email overený",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.full_name or self.email

    class Meta:
        verbose_name = "Používateľ"
        verbose_name_plural = "Používatelia"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(Lower("email"), name="user_email_lower_idx"),
        ]

    def clean(self):
        super().clean()

        if self.email:
            self.email = self.email.lower().strip()

        if not self.first_name:
            raise ValidationError({"first_name": "Meno je povinné"})

        if not self.last_name:
            raise ValidationError({"last_name": "Priezvisko je povinné"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
