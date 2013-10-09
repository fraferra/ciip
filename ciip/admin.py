import logging
from django.contrib import admin
from ciip.models import UserProfile
#from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

#from django.contrib.auth.models import User



class CiipAdmin(admin.ModelAdmin):
   
    model=UserProfile
    
    fieldsets = [
        ('Personal Information', {'fields':['first_name','last_name','email']}),
        ('Academic Information', {'fields':['university']}),
        ('Status Update',{'fields':['status']}),
        ('CV',{'fields':['file_cv']})
    ]
    readonly_fields=['first_name','last_name','email','university']
    list_display = ('first_name', 'last_name','status',)


admin.site.register(UserProfile, CiipAdmin)


#admin.site.unregister(User)

