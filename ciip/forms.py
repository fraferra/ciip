from ciip.models import UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name', 'email','university',)

class StatusUpdateForm(ModelForm):
	class Meta:
		model= UserProfile
        fields = ('status')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()








'''

class UploadFileForm(ModelForm):
	class Meta:
		model=UserProfile
        #exclude =('first_name','last_name','user','university','email','status')
        fields = ('file_cv')'''