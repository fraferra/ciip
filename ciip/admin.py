import logging
from django.contrib import admin
from ciip.models import UserProfile
#from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

#from django.contrib.auth.models import User



class CiipAdmin(admin.ModelAdmin):
   
    model=UserProfile
    
    fieldsets = [
        ('Personal Information', {'fields':['first_name','last_name','passport_number','birth_date_day','birth_date_month','birth_date_year']}),
        ('Contact Information',{'fields':['email','phone','address_line1','address_line2','city','zip_code','country']}),
        ('Academic Information', {'fields':['university','year_of_graduation','degree','average']}),
        ('Motivational Questions', {'fields':['question_1', 'question_2']}),
        ('Status Update',{'fields':['status']}),
        ('CV',{'fields':['file_name','file_cv']})
    ]
    readonly_fields=['first_name','last_name','passport_number','birth_date_day','birth_date_month','birth_date_year','email','phone','address_line1','address_line2','city','zip_code','country','university','year_of_graduation','degree','average','question_1', 'question_2','file_name']
    list_display = ('first_name', 'last_name','status','university')


admin.site.register(UserProfile, CiipAdmin)


#admin.site.unregister(User)

