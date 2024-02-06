from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordForm,
    UserCreationForm,
    PasswordResetForm,
    AuthenticationForm,
)

from .mixins import EmailMixin
from core.apps.library.models import Book  # library app

User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_genre', 'created_by', 'title']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BookForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        form_ = super().save(commit=False)
        form_.created_by = self.request.user
        form_.save()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'your@email.com',
            'id': 'login-username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control font-montreal',
            'placeholder': 'your passwd',
        }
    ))


class UserSignupForm(UserCreationForm, EmailMixin):
    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UserSignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'}
        )

    def save(self, commit=True):
        """Send activation email after creating the user."""
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            self.send_activation_email(self.request, user)
        return user


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'
            }
        ))

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 'placeholder': 'Username',
            }
        ))

    class Meta:
        model = User
        fields = ('email', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = True


class PasswdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find that email address')
        return email


class PasswdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
