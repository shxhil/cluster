from django.forms import ModelForm,Form,CharField
from .models import CustomerReg

class RegistartionForm(ModelForm):

    class Meta:
        model=CustomerReg
        fields="__all__"

class AdminLoginForm(Form):
    username=CharField()
    password=CharField()