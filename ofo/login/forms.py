from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Passwort', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Passwort wiederholen', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) > 30:
            raise forms.ValidationError('Username is too long')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username %s already exists.' % username)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError('Password was not confirmed correctly')
        else:
            return password1


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput)

