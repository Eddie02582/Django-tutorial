from django import forms
from .models import Hardware,RF
from django.forms import inlineformset_factory

class HardwareConfigForm(forms.ModelForm):   
    class Meta:       
        model = Hardware         
        fields=['project']

class RFForm(forms.ModelForm):   
    class Meta:       
        model = RF 
        fields='__all__' 
       

  
RFFormSet = inlineformset_factory(
    Hardware,RF, form=RFForm,
    extra=3, can_delete=True
    )

