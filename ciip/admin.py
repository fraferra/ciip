import logging
from django.contrib import admin
from ciip.models import UserProfile
from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

#from django.contrib.auth.models import User



class CiipAdmin(admin.ModelAdmin):
  

    model=UserProfile
    
    fieldsets = [
        ('University Endorsement',{'fields':['university_endorsement']}),
        ('Personal Information', {'fields':['gender','passport','first_name','last_name']}),#'passport_number','birth_date','birth_date_day','birth_date_month','birth_date_year']}),

        ('Contact Information',{'fields':['email','phone','address_line1','address_line2','city','zip_code','country']}),
        ('Emergency Contact Information',{'fields':['full_name_emergency','relationship','phone_emergency','email_emergency']}),
        ('Academic Information', {'fields':['university','year_of_graduation','degree','average', 'good_university']}),
        ('Motivational Questions', {'fields':['question_1', 'question_2','question_3']}),
        ('Status Update',{'fields':['status']}),
        ('CV',{'fields':['file_name','file_cv']}),
        ('Cover Letter',{'fields':['cover_letter']}),
        ('Work',{'fields':['experience_1','experience_2']}),
        ('Internships',{'fields':['internship_1', 'internship_2']}),
       # ('Image', {'fields':['image']}),
        ('Skills',{'fields':['skill_1','skill_level_1','skill_2',
            'skill_level_2','skill_3','skill_level_3']}),
        ('Interests',{'fields':['interest_1','interest_2','interest_3']}),
    ]
    #readonly_fields=['gender','first_name','last_name','passport_number','birth_date_day','birth_date_month','birth_date_year','email','phone','address_line1','address_line2','city','zip_code','country']
    readonly_fields=['gender','passport','first_name','last_name',
    'birth_date_day','birth_date_month','birth_date_year','email','phone','internship_1', 'internship_2',
    'address_line1','address_line2','city','zip_code','country','university','experience_1','experience_2',
    'year_of_graduation','degree','average','question_1', 'question_2','question_3','file_name',
    'skill_1','skill_level_1','skill_2','skill_level_2','skill_3','skill_level_3','good_university',
    'interest_1','interest_2','interest_3','university_endorsement','full_name_emergency','relationship','phone_emergency','email_emergency','birth_date']
    list_display = ('first_name', 'last_name','status','university','user_email')
    list_filter = ['university', 'status','university_endorsement']


    def user_email(self, instance):
        return instance.user.email
    

admin.site.register(UserProfile, CiipAdmin)


#admin.site.unregister(User)

