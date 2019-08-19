from django import forms

from .models import siteUsers

from .globals import site

from datetime import date, datetime, time

from django.core.exceptions import ValidationError

class loginForm(forms.Form):

    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250)

    def login(self):

        try:

            result = siteUsers.objects.filter(login=login, password=password)[0].login;

            if result: return True

        except: return False

    class Meta:
        model = siteUsers
        fields = ['login', 'email', 'password']

        widgets = {
            'login': forms.TextInput(),
            'email': forms.TextInput(),
            'password': forms.TextInput(),
            'body': forms.Textarea()
        }

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

    def clean_password(self):

        if len(self.cleaned_data['password']) <= 7: raise ValidationError(site['messages']['littlepass'])

        elif len(self.cleaned_data['password']) >= 200: raise ValidationError(site['messages']['bigpass'])

        return self.cleaned_data['password']

    def clean_login(self):

        try:

            another = siteUsers.objects.filter(login=self.cleaned_data['login'])

            if another[0].login: raise ValidationError(site['messages']['exists'])

        except:

            if len(self.cleaned_data['login']) <= 4: raise ValidationError(site['messages']['littlelogin'])

            elif len(self.cleaned_data['login']) >= 100: raise ValidationError(site['messages']['biglogin'])

        return self.cleaned_data['login']
