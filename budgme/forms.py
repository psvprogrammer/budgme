

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': _('login or email')}))
    password = forms.CharField(label=_(u"Ваш пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': _('password')}))


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form that lets a user change their password by entering their old
    password.
    """
    old_password = forms.CharField(label=_('Current password'),
                                   widget=forms.PasswordInput(
                                       {
                                           'class': 'form-control',
                                           'placeholder': _('current password')
                                       }
                                   ))
    new_password1 = forms.CharField(label=_('new password'),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': _('new password')
                                        }
                                    ))
    new_password2 = forms.CharField(label=_('repeat new password'),
                                    widget=forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder': _('new password again')
                                    }))
