from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Email'}))
    password1 = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort'}))
    password2 = forms.CharField(label='Passwort wiederholen', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort wiederholen'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) > 30:
            raise forms.ValidationError('Username ist zu lange.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username %s existiert bereits.' % username)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError('Passwort wurde nicht korrekt wiederholt.')
        else:
            return password1


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort'}))
