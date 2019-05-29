"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField   
#from django.db.models import Q

from .models import (
    Dragon_Solo_Sign_Ups, Elder_Solo_Sign_Ups, Elder_Team_Sign_Ups ,Baron_Team_Sign_Ups,
    Baron_League_Rosters, Baron_Players
    )

class CheckDiscordName(forms.Form):
    def clean_discord_name(self):
        data = self.cleaned_data['discord_name']
        # We need to verify Discord names end in #1234 (or some numbers)
        check_area = data[-5:]
        if not ( (check_area[0] == '#') and (check_area[1:].isdigit()) ):
            raise ValidationError( _('Invalid Discord name - should be "DiscordName#1234"'), code='invalid_discord' )
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

# Website Forms
#region 
class Dragon_League_Signup_Form(ModelForm, CheckDiscordName):
    class Meta:
        model = Dragon_Solo_Sign_Ups
        fields = '__all__'
    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super(Dragon_League_Signup_Form, self).clean()
        primary_role = cleaned_data.get('primary_role')
        secondary_role = cleaned_data.get('secondary_role')
        if primary_role and secondary_role: # If both are valid as is
            if primary_role == secondary_role:
                self.add_error('secondary_role', 'Must choose a different role for your secondary role')

class Elder_League_Solo_Signup_Form(ModelForm, CheckDiscordName):
    class Meta:
        model = Elder_Solo_Sign_Ups
        fields = '__all__'
    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super(Elder_League_Solo_Signup_Form, self).clean()
        primary_role = cleaned_data.get('primary_role')
        secondary_role = cleaned_data.get('secondary_role')
        if primary_role and secondary_role: # If both are valid as is
            if primary_role == secondary_role:
                self.add_error('secondary_role', 'Must choose a different role for your secondary role')

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

#endregion

'''
# Admin Forms
class Roster_Filter(ModelForm):
    class Meta:
        model = Baron_League_Rosters
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Roster_Filter, self).__init__(*args, **kwargs)
        self.fields['top_laner'].queryset = Baron_Players.objects.filter(Q(Baron_League_Rosters__isnull=True))
'''