from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'password1': 'Your password must contain at least 8 characters and should not be entirely numeric.',
        }
        widgets = {
            'username': forms.TextInput(attrs={ 'class': 'border-2 '}),
            'email': forms.EmailInput(attrs={'class': 'border-2 '}),
            'first_name': forms.TextInput(attrs={'class':'border-2 '}),
            'last_name': forms.TextInput(attrs={'class': 'border-2 '}),
            'password1': forms.PasswordInput(attrs={'class': 'border-2 '}),
            'password2': forms.PasswordInput(attrs={'class': 'border-2 '}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        if len(password1) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        if not any(c.isupper() for c in password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password1):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password1):
            raise ValidationError("Password must contain at least one numeral")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs ):
        super(AuthForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password']:
           
            self.fields[fieldname].widget.attrs.update({'class': 'px-3 py-2 border-2 border-gray-400 rounded-md w-full'})