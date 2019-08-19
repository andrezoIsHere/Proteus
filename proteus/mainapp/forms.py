from django import forms

from .models import siteUsers

from .globals import site

from datetime import date, datetime, time

from django.core.exceptions import ValidationError

class loginForm(forms.Form):

    login = forms.CharField(max_length = 100)
    password = forms.CharField(max_length = 250)

class newForm(forms.ModelForm):
    class Meta:
        model = siteUsers
        fields = ['login', 'email', 'password']

        widgets = {
            'login': forms.TextInput(),
            'email': forms.TextInput(),
            'password': forms.TextInput(),
            'body': forms.Textarea()
        }

    def clean_login(self):

        if not self.cleaned_data['login'] and not self.cleaned_data['email'] and not self.cleaned_data['password']:
            raise ValidationError(site['messages']['notfulldata'])

        if len(self.cleaned_data['login']) <= 4:
            raise ValidationError(site['messages']['littlelogin'])

        return self.cleaned_data['login']
