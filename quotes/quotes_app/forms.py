from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import Author, Quote, User


class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    born_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    born_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    quote = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    tags = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, label='Email', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password_confirm = forms.CharField(label="Confirm New Password", strip=False,
                                           widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), )

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("The two password fields didn't match.")
        return new_password_confirm
