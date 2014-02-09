import logging
from django.contrib import admin
from ciip.models import UserProfile, UniversityAdmin, Profile
from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

#from django.contrib.auth.models import User



class CiipAdmin(admin.ModelAdmin):
  

    model=UserProfile
    
    fieldsets = [
        ('Interview',{'fields':['interviewer_comment','interviewer_name','leadership','initiative','innovation','adaptability','team_player','cisco_fit','technical_skill','motivation']}),
        ('Status Update',{'fields':['status','date_interview','interview_response']}),
        ('University Endorsement',{'fields':['university_endorsement', 'uni_comment', 'university_role','university_role_name']}),
        ('Personal Information', {'fields':['gender','passport','first_name','last_name']}),#'passport_number','birth_date','birth_date_day','birth_date_month','birth_date_year']}),

        ('Contact Information',{'fields':['email','phone','address_line1','address_line2','city','zip_code','country']}),
        ('Emergency Contact Information',{'fields':['full_name_emergency','relationship','phone_emergency','email_emergency']}),
        ('Academic Information', {'fields':['university','year_of_graduation','degree','average', 'good_university']}),
        ('Work and Internship experiences', {'fields':['experience_1','experience_2','internship_1','internship_2']}),    
        ('Motivational Questions', {'fields':['question_1', 'question_2','question_3']}),
        
        ('CV',{'fields':['file_name','file_cv']}),
       # ('Image', {'fields':['image']}),
        ('Skills',{'fields':['skill_1','skill_level_1','skill_2',
            'skill_level_2','skill_3','skill_level_3']}),
        ('Interests',{'fields':['interest_1','interest_2','interest_3']}),
    ]
    #readonly_fields=['gender','first_name','last_name','passport_number','birth_date_day','birth_date_month','birth_date_year','email','phone','address_line1','address_line2','city','zip_code','country']
    
    readonly_fields=['gender','passport', 'uni_comment','first_name','last_name','university',
    'university_role','university_role_name',
    'birth_date_day','birth_date_month','birth_date_year','email','phone',
    'address_line1','address_line2','city','zip_code','country','experience_1','experience_2','internship_1','internship_2',
    'year_of_graduation','degree','average','question_1', 'question_2','question_3','file_name',
    #'skill_1','skill_level_1','skill_2','skill_level_2','skill_3','skill_level_3',
    'good_university',
    #'interest_1','interest_2','interest_3',
    'university_endorsement','full_name_emergency','relationship','phone_emergency','email_emergency','birth_date']
    

    list_display = ('first_name', 'last_name','status','university','user_email')
    list_filter = ['university', 'status','university_endorsement']
    search_fields=['first_name','last_name']

    def user_email(self, instance):
        return instance.user.email
    

admin.site.register(UserProfile, CiipAdmin)


#admin.site.unregister(User)

class UniAdmin(admin.ModelAdmin):
    model=UniversityAdmin
    fieldsets= [('University',{'fields':['university','first_name','last_name']}),]
    readonly_fields=['university','first_name','last_name']
    list_display = ( 'last_name','university','user_email')
    def user_email(self, instance):
        return instance.user.email
admin.site.register(UniversityAdmin, UniAdmin)

'''
class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    fieldsets=[('User',{'fields':['user_username']})]
    readonly_fields=['user_username']
    list_display = ('user_username')
    def user_username(self, instance):
        return instance.user.username
admin.site.register(Profile, ProfileAdmin)

'''
        