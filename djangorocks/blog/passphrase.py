
from django import forms

class UpdateUser(forms.Form):
    onoma = forms.CharField(required=True)
    pasw = forms.CharField(widget=forms.PasswordInput)
    #pasw = forms.CharField(required=True)

