"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField   

from AscensionESports_Baseline.models import (
    Dragon_Solo_Sign_Ups, Elder_Solo_Sign_Ups, Elder_Team_Sign_Ups ,Baron_Team_Sign_Ups
    )

class CheckDiscordName(forms.Form):
    def clean_discord_name(self):
        data = self.cleaned_data['discord_name']
        # We need to verify Discord names end in #1234 (or some numbers)
        check_area = data[-5:]
        if not ( (check_area[0] == '#') and (check_area[1:].isdigit()) ):
            raise ValidationError( _('Invalid Discord name - should be "DiscordName#1234"'), code='invalid' )
        return data

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class Dragon_League_Signup_Form(ModelForm, CheckDiscordName):
    class Meta:
        model = Dragon_Solo_Sign_Ups
        fields = '__all__'
    captcha = ReCaptchaField()

class Elder_League_Solo_Signup_Form(ModelForm, CheckDiscordName):
    captcha = ReCaptchaField()
    class Meta:
        model = Elder_Solo_Sign_Ups
        fields = '__all__'

class Elder_League_Team_Signup_Form(ModelForm, CheckDiscordName):
    captcha = ReCaptchaField()
    class Meta:
        model = Elder_Team_Sign_Ups
        fields = '__all__'

class Baron_League_Signup_Form(ModelForm,CheckDiscordName):
    captcha = ReCaptchaField()
    class Meta:
        model = Baron_Team_Sign_Ups
        fields = '__all__'