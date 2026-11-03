from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email address"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Phone number"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email