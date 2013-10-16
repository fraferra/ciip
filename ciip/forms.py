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
            'last_name','birth_date_day','birth_date_month',
            'birth_date_year', 'email',
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

#class UploadFileForm(forms.Form):
  #  title = forms.CharField(max_length=50)
  #  file  = forms.FileField()




class SignUpForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    
    class Meta:
        model = User
        fields = ('username', 'email',) 

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user