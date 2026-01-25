from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


BASE_INPUT_CLASS = (
    "w-full rounded-xl bg-white/80 text-[#003D5B] "
    "px-4 py-3 placeholder:text-[#003D5B]/60 "
    "focus:outline-none focus:ring-2 focus:ring-[#EDAE49]"
)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": BASE_INPUT_CLASS,
                "placeholder": "Email",
            }),
            "first_name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS,
                "placeholder": "Meno",
            }),
            "last_name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS,
                "placeholder": "Priezvisko",
            }),
        }

    password1 = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(attrs={
            "class": BASE_INPUT_CLASS,
            "placeholder": "Heslo",
        }),
    )

    password2 = forms.CharField(
        label="Heslo znova",
        widget=forms.PasswordInput(attrs={
            "class": BASE_INPUT_CLASS,
            "placeholder": "Heslo znova",
        }),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False

        if commit:
            user.save()

        return user
