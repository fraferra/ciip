from ciip.models import UserProfile, UniversityAdmin, ManagerProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User










import string
class PasswordField(forms.CharField):
    
    # Setup the Field
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(min_length = 7, required = True,
                        label = u'Password',
                        widget = forms.PasswordInput(render_value = False),       
                        *args, **kwargs)
    
    # Validate - 1+ Numbers, 1+ Letters
    def clean (self, value):
        
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False

        # Loop until we Match        
        for char in value: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if numCheck and charCheck:
                break
        
        if not numCheck or not charCheck:
            raise forms.ValidationError(u'Your password must include at least \
                                          one letter and at least one number.')

        return super(PasswordField, self).clean(value)



class WorkForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('experience_1','experience_2','internship_1','internship_2')



class EmergencyForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name_emergency','relationship','phone_emergency','email_emergency')

class SignUpFormManager(UserCreationForm):
    email = forms.EmailField(label='Email address', max_length=75)
    password1=PasswordField()
    password2=PasswordField()
    class Meta:
        model = User
        fields = ('username','email') 
    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email


class CoverForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cover_letter',)



class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender','first_name',
            'last_name',#'birth_date_day','birth_date_month',
            #'birth_date',
            'passport',
             'email',
            'phone','address_line1',
            'address_line2','city',
            'zip_code','country',
         
           #'full_name_emergency','relationship','phone_emergency','email_emergency'
           )

class StatusUpdateForm(ModelForm):
	class Meta:
		model= UserProfile
        fields = ('status')

class UploadFileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =('file_name', 'file_cv')


class ds7002Form(ModelForm):
    class Meta:
        model = ManagerProfile
        fields =( 'ds_7002' ,)

'''
class ImageForm(ModelForm):
    class Meta:
        model=UserProfile
        fields= ('image',)
'''

class MotivationalQuestionForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('question_1', 'question_2','question_3')

class AcademicForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('university','year_of_graduation', 'degree','average','good_university')

#class UploadFileForm(forms.Form):
  #  title = forms.CharField(max_length=50)
  #  file  = forms.FileField()


class SkillForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('skill_1','skill_level_1','skill_2',
            'skill_level_2','skill_3','skill_level_3',)

class InterestForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=('interest_1','interest_2','interest_3')
'''
class SignUpForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    password1=PasswordField()
    password2=PasswordField()
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

'''
class EndorsementForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'university_endorsement',)

class UnicommentForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('uni_comment','university_role','university_role_name','university_endorsement')



class UniAdminForm(ModelForm):
    class Meta:
        model=UniversityAdmin
        fields=('first_name','last_name')
            



class SignUpFormAdmin(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    password1=PasswordField()
    password2=PasswordField()
    user_type = forms.ChoiceField( label='User type',choices=(
    
    ('University Admin', 'University Admin'),
    ))
    passcode = forms.CharField(label='Please enter the passcode sent by the CIIP Team:', max_length=10)
    class Meta:
        model = User
        fields = ('username','email','user_type',) 

    def clean_usertype(self):
        user_type=self.cleaned_data["user_type"]

        try:
            user=User.objects.get(user_type=user_type)
        except User.DoesNotExist:
            return user_type
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
        user.user_type = self.cleaned_data["user_type"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
        
        setattr(user, "user_type", self.cleaned_data["user_type"])
        return user



class SignUpForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    password1=PasswordField()
    password2=PasswordField()
    user_type = forms.ChoiceField( label='User type',choices=(
    ('Student', 'Student'),
    
    ))
    class Meta:
        model = User
        fields = ('username','email','user_type',) 

    def clean_usertype(self):
        user_type=self.cleaned_data["user_type"]

        try:
            user=User.objects.get(user_type=user_type)
        except User.DoesNotExist:
            return user_type
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
        user.user_type = self.cleaned_data["user_type"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
        
        setattr(user, "user_type", self.cleaned_data["user_type"])
        return user


