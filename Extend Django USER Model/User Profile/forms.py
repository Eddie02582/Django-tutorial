from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
   
    Team_CHOICES = (
        ('PL', 'PL'),       
		('HW', 'HW'), 
		('Layout', 'Layout'), 
		('Validation', 'Validation'),
		('Automation', 'Automation'), 
		('Others', 'Others'),  			
	) 
    username = forms.CharField(max_length=30, required=True, help_text='輸入工號')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    ext = forms.CharField(max_length=10, required=False, help_text='Optional',initial=" ")	   
    Team = forms.ChoiceField(required=True,choices=Team_CHOICES)   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','Team','email','ext','password1', 'password2')
		

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')		
		
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Team', 'Ext','incumbent')		