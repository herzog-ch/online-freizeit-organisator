from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    """Form for registration of new users

        The clean_username is called when is_valid() is called on the form object.
        It is only tested if the username already exists.
        Email duplication is not tested on purpose for creating multiple during demo

    """
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Email'}))
    password1 = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort'}))
    password2 = forms.CharField(label='Passwort wiederholen', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort wiederholen'}))

    def clean_username(self):
        """Returns the username if the name is not longer than 30 characters and doesn't exist yet.
        Otherwise it will raise an ValidationError

        :return: cleaned username
        """
        username = self.cleaned_data['username']

        if len(username) > 30:
            raise forms.ValidationError('Username ist zu lange.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username %s existiert bereits.' % username)

    def clean_password2(self):
        """Test if the password was input correctly twice. Otherwise a ValidationError is raised"""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError('Passwort wurde nicht korrekt wiederholt.')
        else:
            return password1


class LoginForm(forms.Form):
    """The Login form existing of two input char fields for username and password"""
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                              'placeholder': 'Username'}))
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Passwort'}))
