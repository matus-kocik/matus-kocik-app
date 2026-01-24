from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Concat


class CustomUserManager(BaseUserManager):
    """
    User manager that uses email as the primary identifier instead of username.
    Handles creation of regular users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and persist a regular user identified by email.
        """
        if not email:
            raise ValueError("The Email field is required and must be set")

        # Normalize email to lowercase
        email = self.normalize_email(email)
        # Ensure users are active by default
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)

        if password:
            # Securely set hash the user's password
            user.set_password(password)
        else:
            # Set an unusable password (e.g., for OAuth users...)
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser with staff and superuser permissions enabled.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        """
        Enable case-insensitive lookup by email for authentication.
        """
        if not email:
            raise ValueError("Natural key (email) must be provided")
        # Case-insensitive lookup
        return self.get(email__iexact=email)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the unique login identifier.
    """

    # Model field notes:
    # - verbose_name: label shown in Django admin and forms
    # - help_text: helper text displayed under the input field
    # - db_index: improves performance for frequent lookups (e.g. login)
    email = models.EmailField(
        unique=True,
        db_index=True,  # Optimizes queries involving email searches
        verbose_name="Email Address",  # Display name in Django Admin and forms
        # Appears in Django Admin as field description
        help_text="User's unique email address.",
    )
    first_name = models.CharField(
        max_length=64, verbose_name="First Name", help_text="User's first name."
    )
    last_name = models.CharField(
        max_length=64, verbose_name="Last Name", help_text="User's last name."
    )
    full_name = models.GeneratedField(
        expression=Concat(
            models.F("first_name"), models.Value(" "), models.F("last_name")
        ),
        output_field=models.CharField(max_length=128),
        # Ensures that the full name is stored in the database for optimized queries
        db_persist=True,
        verbose_name="Full Name",
        help_text="User's full name (first + last name).",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active User",
        help_text="Indicates whether the user account is active.",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff User",
        help_text="Indicates whether the user has admin privileges.",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Joined",
        help_text="Timestamp when the user registered.",
    )

    objects = CustomUserManager()

    # Django authentication settings
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        """
        Human-readable representation used in admin and logs.
        """
        return f"{self.full_name} ({self.email})"

    class Meta:
        """
        Admin and database configuration for the user model.
        """

        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def clean(self):
        """
        Normalize and validate user data before saving.
        Ensures lowercase email and avoids case-sensitive duplicates.
        """
        super().clean()

        # Ensure email is lowercase and stripped of whitespace
        if self.email:
            self.email = self.email.lower().strip()

        if not self.first_name:
            raise ValidationError({"first_name": "The First Name field is required"})

        if not self.last_name:
            raise ValidationError({"last_name": "The Last Name field is required"})

        # Ensure email uniqueness (Django already enforces unique=True,
        # but this prevents case-sensitive issues)

        if CustomUser.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError({"email": "A user with this email already exists."})
