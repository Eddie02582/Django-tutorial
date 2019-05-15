from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse,render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,permission_required

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView,CreateView,ListView
from django_tables2 import RequestConfig
from django.core.mail import send_mail
from .forms import SignUpForm,UserForm,ProfileForm
from .models import 	Profile
from django.db import transaction	
from django.contrib.messages import constants as messages
from django.contrib.auth.models import Group
#CBV	
class SignupView(CreateView):
    model = User
    form_class = SignUpForm  
    template_name = 'signup.html'
	
    def form_valid(self, form):
        team=form.cleaned_data.get('Team')
        user = form.save()
        user.refresh_from_db()  # load the profile instance created by the signal
        user.profile.Team = team
        user.profile.Ext = form.cleaned_data.get('Ext')  
        group = Group.objects.get(name=team)		
        user.groups.add(group)        
        user.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(self.request, user)
        return redirect('HomePage')	

	
def UserProfile(request,userid):
    user = User.objects.get(username=userid)    
    profile=Profile.objects.get(user=user)
    if request.method == 'POST':       
        return redirect('Profile_Update')	
    return render(request, 'registration/userprofile.html', {'user': request.user,'profile':profile,'profile_user':user})
	


@login_required
@transaction.atomic
def ProfileUpdate(request):
    if request.method == 'POST':        
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('HomePage')				
        else:
            pass
            #messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })	


