from django import forms

from .models import siteUsers

from datetime import date, datetime, time

#from django.core.exceptions import ValidationError

class loginForm(forms.Form):

    login = forms.CharField(max_length = 100)
    password = forms.CharField(max_length = 250)

class regForm(forms.ModelForm):

    login = forms.CharField(max_length = 100)
    email = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 250)
    karma = forms.IntegerField()

    class Meta:

        model = siteUsers
        fields = ['login', 'email', 'password', 'karma']

        widgets = {
            'login': forms.TextInput(attrs={'class': 'form__input'}),
            'email': forms.TextInput(attrs={'class': 'form__input'}),
            'password': forms.TextInput(attrs={'class': 'form__input'})
        }

    def clean_email(self):
        new = self.data['email'].lower()

        return new

#    def save(self):
#
#        new = siteUsers.objects.create(
#            login=self.data['login'],
#            email=self.data['email'],
#            password=self.data['password'],
#            karma=self.data['karma']
#        )
