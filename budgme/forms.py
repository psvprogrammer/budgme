

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'логін або email'}))
    password = forms.CharField(label=_(u"Ваш пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': u'пароль'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form that lets a user change their password by entering their old
    password.
    """
    old_password = forms.CharField(label=_(u"Поточний пароль"),
                                   widget=forms.PasswordInput(
                                       {
                                           'class': 'form-control',
                                           'placeholder': u'поточний пароль'
                                       }
                                   ))
    new_password1 = forms.CharField(label=_(u"Новий пароль"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'новий пароль'
                                        }
                                    ))
    new_password2 = forms.CharField(label=_(u"Повторіть новий пароль"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'новий пароль ще раз'
                                        }
                                    ))