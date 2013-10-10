from ciip.models import UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender','first_name',
            'last_name','birth_date_day','birth_date_month','birth_date_year', 'email',
            'phone','address_line1',
            'address_line2','city',
            'zip_code','country',
            'passport_number')

class StatusUpdateForm(ModelForm):
	class Meta:
		model= UserProfile
        fields = ('status')

class UploadFileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =('file_name', 'file_cv')

    

class MotivationalQuestionForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('question_1', 'question_2')

class AcademicForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('university','year_of_graduation', 'degree','average')

'''class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
'''




