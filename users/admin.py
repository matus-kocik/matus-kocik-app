from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Potvrdenie hesla", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Heslá sa nezhodujú.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=(
            "Heslá nie sú uložené v čitateľnej podobe, preto ich nie je možné zobraziť. Heslo môžete zmeniť pomocou <a href=\"../password/\">tohto formulára</a>."
        )
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ["email", "full_name", "email_verified", "is_active", "is_staff", "date_joined"]
    list_display_links = ["email", "full_name"]
    list_editable = ["is_active", "is_staff"]
    search_fields = ["email__icontains", "first_name__icontains", "last_name__icontains"]
    list_filter = ["email_verified", "is_active", "is_staff", "date_joined"]
    ordering = ["-date_joined"]
    list_per_page = 25
    list_select_related = ()
    date_hierarchy = "date_joined"
    readonly_fields = ["date_joined", "last_login"]
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Osobné údaje", {"fields": ("first_name", "last_name", "email_verified")} ),
        (
            "Oprávnenia",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dôležité údaje", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Nový používateľ",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
