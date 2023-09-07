from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Korisnici,Predmeti, Upisi
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class PredmetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PredmetForm, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = Korisnici.objects.filter(uloga='PROFESOR')
    class Meta:
        exclude = []
        model = Predmeti

class StudentForm(UserCreationForm):
    def __init__(self, *args,**kwargs):
        super(StudentForm, self).__init__(*args,**kwargs)
        self.initial['uloga'] = Korisnici.objects.filter(uloga='STUDENT')
    class Meta:
        model = Korisnici
        fields = ['first_name', 'last_name', 'email', 'username','uloga', 'status']

class ProfesorForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        super(ProfesorForm,self).__init__(*args,**kwargs)
        self.initial['uloga'] = Korisnici.objects.filter(uloga='PROFESOR')
    class Meta:
        model = Korisnici
        fields = ['first_name', 'last_name','email','username','uloga']

class UpisiForm(forms.ModelForm):
    class Meta:
        model = Upisi
        fields = ['korisnici', 'predmeti','status']

#forma za LogIn
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)