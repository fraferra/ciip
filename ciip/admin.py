import logging
from django.contrib import admin
from ciip.models import *
from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin
import requests
#from django.contrib.auth.models import User
import xlsxwriter
from django.http import HttpResponse

class CiipAdmin(admin.ModelAdmin):
  

    model=UserProfile
    
    fieldsets = [
        ('User',{'fields':['user','listed','offer_states', 'is_open', 'is_returning']}),
        ('Second Stage',{'fields':['technical_resume_screen_selection','technical_resume_screen_comment','technical_interview_screen_selection','technical_interview_screen_comment','master_or_undergrad']}),
        ('Interview',{'fields':['interviewer_comment','interviewer_name','position_suggested','leadership','initiative','innovation','adaptability','team_player','cisco_fit','technical_skill','motivation']}),
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
        ('Visa Documents',{'fields':['ds_2019']}),
    ]
    #readonly_fields=['gender','first_name','last_name','passport_number','birth_date_day','birth_date_month','birth_date_year','email','phone','address_line1','address_line2','city','zip_code','country']
    
    readonly_fields=['passport', 'first_name','last_name','gender',
    'interview_response',
    'file_cv','ds_2019',
    'offer_states','file_cv',
    'technical_resume_screen_selection','technical_resume_screen_comment','technical_interview_screen_selection','technical_interview_screen_comment',
    'interviewer_comment','interviewer_name',
    'date_interview',
    'university_role','university_role_name','uni_comment',
    'birth_date_day','birth_date_month','birth_date_year','phone',
    'address_line1','address_line2','city','zip_code','experience_1','experience_2','internship_1','internship_2',
    'average','question_1', 'question_2','question_3','file_name',
    'skill_1','skill_level_1','skill_2','skill_level_2','skill_3','skill_level_3',
    'good_university',
    'interest_1','interest_2','interest_3',
    'university_endorsement',
    'full_name_emergency','relationship','phone_emergency','email_emergency','birth_date']
    

    list_display = ('first_name', 'last_name','status','university','user_email','user_name')
    list_filter = ['university', 'status','university_endorsement', 'master_or_undergrad']
    search_fields=['first_name','last_name', ]
    actions=['change_to_no','print_report']

    def user_email(self, instance):
        return instance.user.email
    def user_name(self, instance):
        return instance.user.username

    def change_to_no(modeladmin, request, queryset):
        for query in queryset:
            query.listed = 'no'
            query.save()

    change_to_no.short_description = "Change to no"


    def print_report(modeladmin, request, queryset):
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO
        output = StringIO.StringIO()
        title='report_students'  
        workbook=xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Full Name', bold)
        worksheet.write('B1', 'Email', bold)
        worksheet.write('C1', 'University', bold)
        worksheet.write('D1', 'Country', bold)
        worksheet.set_column('A:D', 20)
        row=2
        ordered_list=queryset.order_by('university')
        for query in ordered_list:
            worksheet.write('A'+str(row),unicode(query.first_name) +' '+ unicode(query.last_name))
            worksheet.write('B'+str(row), query.user.email)
            worksheet.write('C'+str(row), query.university)
            worksheet.write('D'+str(row), query.country)
            row=row+1
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename="+title
        return response

    print_report.short_description = "Print report"

admin.site.register(UserProfile, CiipAdmin)


#admin.site.unregister(User)

class UniAdmin(admin.ModelAdmin):
    model=UniversityAdmin
    fieldsets= [('user',{'fields':['user']}),('University',{'fields':['university','first_name','last_name']}),]
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
        
class ManagerAdmin(admin.ModelAdmin):
    model=ManagerProfile
    fieldsets=[('DS7002 Info', {'fields':['job_title','group','degree','field','year_experience']}),
    ('General Info', {'fields':['user','business_unit','first_name','last_name','coordinator', ]}),
    ('Interests and Skills', {'fields':['skill_1','skill_2','skill_3','interest_1','interest_2','interest_3','work_description']})]
    list_display = ( 'last_name','business_unit','user_email')
    readonly_fields=['work_description', 'skill_1','skill_2','skill_3','interest_1','interest_2','interest_3']
    actions=['print_report',]
    def user_email(self, instance):
        return instance.user.email

    def print_report(modeladmin, request, queryset):
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO
        output = StringIO.StringIO()
        title='report_managers'  
        workbook=xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Full Name', bold)
        worksheet.write('B1', 'Email', bold)
        worksheet.write('C1', 'Business Unit', bold)
        worksheet.write('D1', 'VAP', bold)
        worksheet.write('F1', '# Interns', bold)
        worksheet.set_column('A:F', 20)
        row=2
        for query in queryset:
            worksheet.write('A'+str(row),query.first_name +' '+ query.last_name)
            worksheet.write('B'+str(row), query.user.email)
            worksheet.write('C'+str(row), query.business_unit)
            worksheet.write('D'+str(row), query.vap)
            worksheet.write('F'+str(row), query.number_interns)
            row=row+1
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename="+title
        return response

    print_report.short_description = "Print report"

admin.site.register(ManagerProfile,ManagerAdmin)

class InterviewAdmin(admin.ModelAdmin):
    model=Interview
    fieldsets=[('Info',{'fields':['date','student','manager','interview_response']}),]
    readonly_fields=['date','student','manager','interview_response']

admin.site.register(Interview,InterviewAdmin)

class MessageAdmin(admin.ModelAdmin):
    model=Message
    fieldsets=[('Info',{'fields':['text','student','manager']}),]
    readonly_fields=['text','student','manager']

admin.site.register(Message,MessageAdmin)





