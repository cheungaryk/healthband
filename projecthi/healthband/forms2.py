from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Patient, Provider

class RegistrationForm(ModelForm):
    username        = forms.CharField(label=(u'User Name'))
    email           = forms.EmailField(label=(u'Email Address'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Patient
        exclude = ('user', 'pid', 'blood_type')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That username is already taken, please select another.")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("The passwords did not match.  Please try again.")
        return self.cleaned_data

class LoginForm(forms.Form):
        username        = forms.CharField(label=(u'User Name'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

class providerRegistrationForm(forms.ModelForm):

    first_name      = forms.CharField(label=(u"First Name"))
    last_name      = forms.CharField(label=(u"Last Name"))
    username        = forms.CharField(label=(u'User Name'))
    email           = forms.EmailField(label=(u'Email Address'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Provider
        exclude = ['user', 'hContactEmail']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That username is already taken, please select another.")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("The passwords did not match.  Please try again.")
        return self.cleaned_data
