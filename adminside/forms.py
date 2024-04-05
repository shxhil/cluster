from django import forms
from publicuser.models import CustomerReg

class AdminLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model=CustomerReg
        exclude=["username","password","conform_password"]

class UploadForm(forms.Form):
    file=forms.FileField()