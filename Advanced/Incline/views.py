from django.shortcuts import render
from .models import HWGroup,Hardware,RF
from .forms import HardwareConfigForm,RFFormSet
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.

 
    

class HWConfig(CreateView):
    model = Hardware
    form_class=HardwareConfigForm	
    template_name = 'HwConfig.html'
	
    def get_context_data(self, **kwargs):
        context = super(HWConfig, self).get_context_data(**kwargs)
        if self.request.POST:
            context['incline_form'] = RFFormSet(self.request.POST)            
        else:
            context['incline_form'] = RFFormSet()           
        return context    
        
        
class RFCreate(CreateView):
    model = RF
    fields = ['chip_type', 'recieve','transmit']