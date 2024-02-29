from django.contrib.auth.forms import UserCreationForm
from scrapapp.models import UserProfile
from django import forms
from django.contrib.auth.models import User
from scrapapp.models import UserProfile,Scrap,Category,Bids


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class ScrapForm(forms.ModelForm):
    class Meta:
        model=Scrap
        fields=['name','price','condition','picture','place','category']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # 'picture': forms.ImageField(attrs={'class': 'form-control'})
        }

class BidsForm(forms.ModelForm):
    class Meta:
        model=Bids
        fields=['amount']


