# Create your views here.
import smtplib
import os
import re
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
#import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
from ciip.forms import  StatusUpdateForm  ,UserProfileForm , EndorsementForm, UnicommentForm, SignUpFormAdmin, UniAdminForm , WorkForm, CoverForm, UploadFileForm, AcademicForm, MotivationalQuestionForm, SignUpForm,  SkillForm, InterestForm
from django.http import HttpResponseRedirect, HttpResponse
from ciip.models import *
#from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required, permission_required

from pytz import timezone 
#from django.utils import timezone
from django.views.generic import FormView
from django import forms, http
from functions import *



def signup(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            email=request.POST['email']
            if checkemail(email):
                new_user = form.save() 
                return HttpResponseRedirect('/ciip/login/')
            else:
                return HttpResponseRedirect('/ciip/notactive/')        
    else:
        form = SignUpForm()
        
    return render( request, 'ciip/signup.html', {
        'form': form, 'user_name':user_name 
    })


def login(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/ciip/home/')
            else:
                return HttpResponseRedirect('ciip/notactive/')
        else:
            return HttpResponseRedirect('/ciip/notregistered/')
    return render(request, 'ciip/login.html', {'username':username, 'password':password,'user_name':user_name})


def logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/login/')

def intern_profiles(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request, 'ciip/intern_profiles.html',{'user_name':user_name})

def notactive(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    if request.method =='POST':
        return HttpResponseRedirect('ciip/eligibility/')
    return render(request, 'ciip/notactive.html',{'user_name':user_name})

def notregistered(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    if request.method =='POST':
        return HttpResponseRedirect('/ciip/eligibility/')
    return render(request, 'ciip/notregistered.html',{'user_name':user_name})

def edit_contact_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        profile = UserProfile.objects.get(user = request.user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST or None, instance=request.user.get_profile())
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.id
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/ciip/profile_contact_info/')
        else:
            form = UserProfileForm(instance=request.user.get_profile())
    return render( request, 'ciip/edit_contact_info.html', {
        'form': form, 'user_name':user_name,
    })



def profile_contact_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
            first_name= profile.first_name
            last_name = profile.last_name
            email= profile.email
            gender=profile.gender
            passport=profile.passport
            #birth_date_day=profile.birth_date_day
            #birth_date_month=profile.birth_date_month
            #birth_date_year=profile.birth_date_year
            address_line1=profile.address_line1
            address_line2=profile.address_line2
            phone=profile.phone
            city=profile.city
            zip_code=profile.zip_code
            country=profile.country
            #passport_number=profile.passport_number
            #full_name_emergency=profile.full_name_emergency
            #birth_date=profile.birth_date
            #date_issued=profile.date_issued
            #country_issued=profile.country_issued
            #date_expiration=profile.date_expiration
            #email_emergency=profile.email_emergency
            #phone_emergency=profile.phone_emergency
            #relationship=profile.relationship


            contact_info={'user_name':user_name,'passport':passport ,'first_name':first_name,'last_name':last_name,
            'email':email,#'birth_date':birth_date,'birth_date_day':birth_date_day,'birth_date_year':birth_date_year,'birth_date_month':birth_date_month,
            'gender':gender, 'address_line1':address_line1,
            'address_line2':address_line2, 'phone':phone,
            'city':city, 'zip_code':zip_code,
            'country':country,# 'passport_number':passport_number,
            #'full_name_emergency':full_name_emergency, #'date_expiration':date_expiration,
            #'date_issued':date_issued, 'country_issued':country_issued,
            #'email_emergency':email_emergency, 'phone_emergency':phone_emergency,
            #'relationship':relationship,
            }
    return render(request, 'ciip/profile_contact_info.html', contact_info)




def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
        try:
            current_pk = request.user.pk
            user_name = User.objects.get(pk=current_pk).username
            status = UserProfile.objects.get(user = request.user).status
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ciip/uniadmin_login/') 
        #if request.method =='GET':
            #profile = UserProfileForm(instance=request.user.get_profile())
            #user_name=str(profile['first_name'])
            #status_profile = StatusUpdateForm(instance=request.user.get_profile())
            #status=status_profile['status']
            
            
            
    return render(request, 'ciip/home.html', {'user_name': user_name,'status':status,})


def eligibility(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/eligibility.html',{'user_name':user_name})
'''
def upload_file(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       if request.method == 'POST':
           form = UploadFileForm(request.POST, request.FILES, instance=request.user.get_profile())
           if form.is_valid():
            # file is saved
               new_user=form.save()
               return HttpResponseRedirect('/ciip/upload_file/')
       else:
           form = UploadFileForm(instance=request.user.get_profile())
    return render(request, 'ciip/upload_file.html', {'form': form,'user_name':user_name})
'''


def upload_file(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       if request.method == 'GET':
           profile = UserProfile.objects.get(user = request.user)
           cv=profile.file_cv
    return render(request, 'ciip/upload_file.html', {'cv': cv,'user_name':user_name})



def cover_letter(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       if request.method == 'POST':
           form = CoverForm(request.POST, request.FILES, instance=request.user.get_profile())
           if form.is_valid():
            # file is saved
               new_user=form.save()
               return HttpResponseRedirect('/ciip/cover_letter/')
       else:
           form = CoverForm(instance=request.user.get_profile())
    return render(request, 'ciip/cover_letter.html', {'form': form,'user_name':user_name})





def send_email(request):
    return render(request,'ciip/contact_us.html')
    '''subject=message=from_email=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/contact_us/')
    else: 
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       email = User.objects.get(pk=current_pk).email
       if request.method=='POST':
           subject = request.POST.get('subject','')
           message = request.POST.get('message','')+' sent by '+email+'. Copy and paste address to answer.'
           from_email = email
           if subject and message and from_email:
               try:
                   send_mail(subject, message, from_email , ['ciip.team.1@gmail.com'])
               except BadHeaderError:
                   return HttpResponse('Invalid header found.')
               return HttpResponseRedirect('/ciip/home/')
       #else:
        # In reality we'd use a form class
        # to get proper validation errors.
         #  return HttpResponse('Make sure all fields are entered and valid.')
    return render(request,'/ciip/send_email.html', {'subject':subject,
                                                    'user_name':user_name, 
                                                    'message':message,
                                                    })'''



def academic_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
            year_of_graduation= profile.year_of_graduation
            degree = profile.degree
            average= profile.average
            university = profile.university
            good_university=profile.good_university
            contact_info={'user_name':user_name,'good_university':good_university, 'year_of_graduation':year_of_graduation,'degree':degree,'average':average,'university':university}
    return render(request, 'ciip/academic_info.html', contact_info)



def edit_academic_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method == 'POST':

            form = AcademicForm(request.POST or None, instance=request.user.get_profile())
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.id
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/ciip/academic_info/')
        else:
            form = AcademicForm(instance = request.user.get_profile())
    return render( request, 'ciip/edit_academic_info.html', {
        'form': form, 'user_name':user_name,
    })


def work_internship(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
            experience_1= profile.experience_1
            experience_2 = profile.experience_2
            internship_1 = profile.internship_1
            internship_2 = profile.internship_2
            
            contact_info={'user_name':user_name,'internship_1':internship_1,'internship_2':internship_2, 'experience_1':experience_1,'experience_2':experience_2}
    return render(request, 'ciip/work_internship.html', contact_info)

def edit_work_internship(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method == 'POST':

            form = WorkForm(request.POST or None, instance=request.user.get_profile())
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.id
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/ciip/work_internship/')
        else:
            form =WorkForm(instance = request.user.get_profile())
    return render( request, 'ciip/edit_work_internship.html', {
        'form': form, 'user_name':user_name,
    })




def motivational_questions(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
            question_1= profile.question_1
            question_2 = profile.question_2
            question_3 = profile.question_3
            contact_info={'user_name':user_name,'question_1':question_1,'question_2':question_2,'question_3':question_3}
    return render(request, 'ciip/motivational_questions.html', contact_info)


def edit_motivational_questions(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method == 'POST':

            form = MotivationalQuestionForm(request.POST or None, instance=request.user.get_profile())
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.id
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/ciip/motivational_questions/')
        else:
            form = MotivationalQuestionForm(instance = request.user.get_profile())
    return render( request, 'ciip/edit_motivational_questions.html', {
        'form': form, 'user_name':user_name,
    })




'''
def upload_image(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       if request.method == 'POST':
           form = ImageForm(request.POST, request.FILES, instance=request.user.get_profile())
           if form.is_valid():
            # file is saved
               new_user=form.save()
               return HttpResponseRedirect('/ciip/upload_image/')
       else:
           form = ImageForm(instance=request.user.get_profile())
    return render(request, 'ciip/upload_image.html', {'form': form,'user_name':user_name})
'''

def edit_skill_interest(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method == 'POST':

            form = SkillForm(request.POST or None, instance=request.user.get_profile())
            form2= InterestForm(request.POST or None, instance=request.user.get_profile())
            if form.is_valid() and form2.is_valid:
                new_user = form.save()
                new_user2 = form2.save()
                return HttpResponseRedirect('/ciip/skill_interest/')
        else:
            form = SkillForm(instance = request.user.get_profile())
            form2 = InterestForm(instance= request.user.get_profile())
    return render( request, 'ciip/edit_skill_interest.html', {
        'form': form,'form2': form2, 'user_name':user_name,
    })



def skill_interest(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
            skill_1= profile.skill_1
            skill_2= profile.skill_2
            skill_3= profile.skill_3
            skill_level_1=profile.skill_level_1
            skill_level_2=profile.skill_level_2
            skill_level_3=profile.skill_level_3
            interest_1=profile.interest_1
            interest_2=profile.interest_2
            interest_3=profile.interest_3

            skill_interest={'skill_1':skill_1, 'skill_level_1':skill_level_1, 'skill_2':skill_2,
            'skill_level_2':skill_level_2,'skill_3':skill_3, 'skill_level_3':skill_level_3, 
            'interest_1':interest_1,'interest_2':interest_2,'interest_3':interest_3}


    return render(request, 'ciip/skill_interest.html', skill_interest)


def video(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/video.html', {'user_name':user_name})

def info(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/info.html', {'user_name':user_name})

def faq(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/faq.html',{'user_name':user_name})

def alternative_sign_up(request):
    university = ''
    first_name = ''
    last_name = ''
    email=''
    if request.method=='POST':
           university = request.POST['university']
           first_name = request.POST['first_name']
           last_name = request.POST['last_name']
           email=request.POST['email']
           from_email = email
           if university and first_name and last_name and from_email:
               try:
                   message = first_name + ' '+ last_name + ' from '+ university+' applied through the alternative sign up. Please notify '+university+'. '+first_name+"'s email is "+email
                   send_mail(last_name+' '+ first_name, message, from_email , ['fraferra@cisco.com','elbowen@cisco.com','bmiloshe@cisco.com'])
                   student_message='Dear '+first_name+', your request has been sent. Please wait until further notice from the CIIP Team. The process might take up to one week. Thank you!'
                   to_email=[email]
                   send_mail('message sent!', student_message, 'ciip-office@cisco.com', to_email)
               except BadHeaderError:
                   return HttpResponse('Invalid header found.')
               return HttpResponseRedirect('/ciip/info/')
       #else:
        # In reality we'd use a form class
        # to get proper validation errors.
         #  return HttpResponse('Make sure all fields are entered and valid.')
    return render(request,'/ciip/alternative_sign_up.html', {'university':university,
                                                    'first_name':first_name,
                                                    'last_name':last_name, 
                                                    'email':email,
                                                    })


def contact_us(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/contact_us.html',{'user_name':user_name})


def forgot_password(request):
    email=''
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'ciip/forgot_password.html', {'email':email})


def current_project(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request, 'ciip/current_project.html', {'user_name':user_name})

def interview(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        profile = UserProfile.objects.get(user = request.user)
        date_interview = profile.date_interview
        webex_link = profile.webex_link
        interview_response = profile.interview_response  
        if request.method == 'POST':
            interview_response=request.POST['interview_response']
            profile.interview_response=interview_response
            profile.save()
            return HttpResponseRedirect('/ciip/interview/')
            
    return render(request, 'ciip/interview.html', {'user_name':user_name, 'date_interview':date_interview,
     'webex_link':webex_link, 'interview_response':interview_response})

def my_managers(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
         
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username  
        current_student = UserProfile.objects.get(user = request.user)
        
        
        interviews_with_managers=Interview.objects.filter(student=current_student)
        if request.method == 'POST':
            interview_id=request.GET['id']
            interview_response=request.POST['interview_response']
            interview=Interview.objects.get(pk=interview_id)
            interview.interview_response=interview_response
            interview.save()
            to_email=[interview.manager.user.email]
            from_email=current_student.user.email
            subject='CIIP Interview:'+current_student.last_name+' replied'
            message=current_student.last_name+' replied with '+interview_response+' for the interview at '+str(interview.date)+'. The email of the student:'+current_student.user.email
            sendEmailNotification(from_email, to_email, subject, message)
            return HttpResponseRedirect('/ciip/my_managers/')
    return render(request, 'ciip/my_managers.html', {'user_name':user_name, 'current_student':current_student,'interviews_with_managers':interviews_with_managers})

def student_send_message(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
        manager_id= request.GET['id']
        current_pk = request.user.pk
        current_manager=ManagerProfile.objects.get(pk=manager_id)
        user_name = User.objects.get(pk=current_pk).username   
        current_student = UserProfile.objects.get(user = request.user)
        previous_messages= Message.objects.filter(student=current_student, manager=current_manager).reverse()
        #a = range(len(previous_messages))
        #sorted(previous_messages, key=lambda x: a.index(x.date_sent))
        if request.method =='POST':
            message=request.POST['message']
            time =datetime.now()
            message=Message.objects.create(text=message, manager=current_manager, student=current_student, sent_by=current_student.first_name, date_sent=time)
            return HttpResponseRedirect('/ciip/student_send_message/?id='+manager_id)

    return render(request, 'ciip/student_send_message.html', {'user_name':user_name, 'previous_messages':previous_messages})










































def signup_uniadmin(request):
    usertype=''
    passcode='2860486313'
    if request.method == 'POST':
        form = SignUpFormAdmin(request.POST)
        
        if form.is_valid():
            email=request.POST['email']
            user_passcode = request.POST['passcode']
            #import sys
            #print >> sys.stderr, "********* User Current PK %s" %(user_passcode)
            if checkemail(email) and user_passcode==passcode:
                new_user = form.save()
                
                #UniversityAdmin.objects.create(user=instance) 
                #post_save.connect(models.create_uni_profile, sender=User)  
                return HttpResponseRedirect('/ciip/uniadmin_login/')
            else:
                '''import Tkinter
                import tkMessageBox
                tkMessageBox.showinfo("Say Hello", "Hello World")'''
                return HttpResponseRedirect('/ciip/signup_uniadmin/')        
    else:
        form = SignUpFormAdmin()
        
    return render( request, 'ciip/signup_uniadmin.html', {
        'form': form, 'passcode':passcode,
    })


def uniadmin_login(request):
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/ciip/home_uniadmin/')
            else:
                return HttpResponseRedirect('ciip/notactive/')
        else:
            return HttpResponseRedirect('/ciip/notregistered/')
    return render(request, 'ciip/uniadmin_login.html', {'username':username, 'password':password})





def uniadmin_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')
    else:    
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        
        try:
            profile = UniversityAdmin.objects.get(user=current_user)
            if request.method == 'GET':
            
                
                university = profile.university
                first_name = profile.first_name
                last_name = profile.last_name
                contact_info={'user_name':user_name,'university':university, 'first_name':first_name, 'last_name':last_name}
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ciip/uniadmin_login/')



    return render(request, 'ciip/uniadmin_info.html', contact_info)


def uniadmin_edit_info(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')

    else:
        first_name = last_name = ''
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        profile = UniversityAdmin.objects.get(user=request.user)
        if request.method == 'POST':
            #form = UniAdminForm(request.POST or None, instance=profile.get_profile())
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.idf
            #if form.is_valid():
                #new_user = form.save()
            return HttpResponseRedirect('/ciip/uniadmin_info/')
        #else:
            #form = UniAdminForm(instance = profile.get_profile())
          
        #except ObjectDoesNotExist:
            #return HttpResponseRedirect('/ciip/login/')


    return render( request, 'ciip/uniadmin_edit_info.html', {
         'user_name':user_name,'last_name':last_name, 'first_name':first_name,
    })




def home_uniadmin(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        #for uni_object in UniversityAdmin.objects.all():
        #u = UniversityAdmin.objects.get(user=request.user)



        try:
        #import sys
        #print >> sys.stderr, "********* User Current PK %s" %(current_pk)
            uniadmin_profile = UniversityAdmin.objects.get(user=request.user)
            email = User.objects.get(pk=current_pk).username
            
            getUniAdmin(email, current_user)

        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ciip/login/')
        #if request.method =='GET':
            #profile = UserProfileForm(instance=request.user.get_profile())
            #user_name=str(profile['first_name'])
            #status_profile = StatusUpdateForm(instance=request.user.get_profile())
            #status=status_profile['status']
            
            
            
    return render(request, 'ciip/home_uniadmin.html', {'user_name': user_name,})



def list_student(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        try:
            profile = UniversityAdmin.objects.get(user=request.user)
            university=profile.university
            if request.method == 'GET':
                uni_list=[]
                particular_student = ''
                list_student= UserProfile.objects.all()
                for student in list_student:
                    if student.university == profile.university:
                            #form = EndorsementForm(request.POST or None, instance=student)
                            uni_list.append(student)
                            #university_endorsement=student.university_endorsement
                            #form = EndorsementForm(request.GET or None, instance=student)

                                #university_endorsement = request.POST['student.university_endorsement']
                            #if form.is_valid:
                                #new_user = form.save()
                                #university_endorsement = form.cleaned_data['university_endorsement']
            #else:
                #form = EndorsementForm(instance = student)
            #if request.method == 'POST':       
                #particular_student = request.POST['particular_student']
                #request.session['particular_student'] = particular_student
                #return HttpResponseRedirect('/ciip/student_info/')

        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ciip/login/')



    return render(request, 'ciip/list_student.html', {'university':university,'uni_list':uni_list, 'user_name':user_name, 'particular_student':particular_student})


def student_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username

        try:
            profile = UniversityAdmin.objects.get(user=request.user)
            #particular_student = request.session.get('particular_student')
            particular_student = request.GET['id']
            
            profile_student = UserProfile.objects.get( pk=particular_student)            
            request.session['particular_student'] = profile_student.id
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/ciip/login/')

    return render(request, 'ciip/student_info.html', {'user_name':user_name,
                             'particular_student':particular_student, 'profile_student':profile_student})



def save_unicomment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/uniadmin_login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        #particular_student = request.session.get('particular_student')
        particular_student = request.GET['id']
        profile_student = UserProfile.objects.get(pk=particular_student)
     
        if request.method == 'POST':
            form = UnicommentForm(request.POST or None, instance=profile_student)
            #form2 = EndorsementForm(request.POST or None, instance=profile_student)
          
            if form.is_valid():
                new_user = form.save()
                #new_user2 = form2.save()
                return HttpResponseRedirect('/ciip/student_info/?id='+particular_student)
        else:
            form = UnicommentForm(instance=profile_student)
            #form2 = EndorsementForm(instance=profile_student)
    return render( request, 'ciip/save_unicomment.html', {'form':form,  'user_name':user_name,
     'particular_student':particular_student, 'profile_student':profile_student})





    























'''


#manager views
def manager_signup(request):
    passcode='2860486313'
    if request.method == 'POST':
        form = SignUpFormManager(request.POST)
        
        if form.is_valid():
            email=request.POST['email']
            user_passcode = request.POST['passcode']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            business_unit=request.POST['business_unit']
            skill_1=request.POST['skill_1']
            skill_2=request.POST['skill_2']
            skill_3=request.POST['skill_3']
            interest_1=request.POST['interest_1']
            interest_2=request.POST['interest_2']
            interest_3=request.POST['interest_3']
            #import sys
            #print >> sys.stderr, "********* User Current PK %s" %(user_passcode)
            if checkciscoemail(email) and user_passcode==passcode:
                new_user = form.save()
                user=User.objects.get(email=email)
                ManagerProfile.objects.create(user=user,
                                              first_name=first_name,
                                              last_name=last_name,
                                              business_unit=business_unit,
                                              skill_1=skill_1,
                                              skill_2=skill_2,
                                              skill_3=skill_3,
                                              interest_1=interest_1,
                                              interest_2=interest_2,
                                              interest_3=interest_3
                    )

                return HttpResponseRedirect('/ciip/manager_login/')
            else:
                return HttpResponseRedirect('/ciip/manager_signup/')        
    else:
        form = SignUpFormManager()
        
    return render( request, 'ciip/manager_signup.html', {
        'form': form, 'passcode':passcode,
    })



def manager_login(request):
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/ciip/manager_home/')
            else:
                return HttpResponseRedirect('ciip/notactive/')
        else:
            return HttpResponseRedirect('/ciip/notregistered/')
    return render(request, 'ciip/manager_login.html', {'username':username, 'password':password})

def manager_home(request):
    results=[]
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        try:
            manager_profile = ManagerProfile.objects.get(user=request.user)
            previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
            #algorithm=functions()
            top_3=matchingAlgorith(manager_profile)
            delete_interview=request.GET.get('delete','')
            if len(delete_interview) !=0:
                interview=Interview.objects.get(pk=delete_interview)
                interview.delete()
                return HttpResponseRedirect('/ciip/manager_home')

            try:
                query=request.GET['search']
                results=search_student(query)
                
            except MultiValueDictKeyError:
                pass
            try:
                filter_result=request.GET['sort']
                results=returnConfirmedOrNot(filter_result)
                
            except MultiValueDictKeyError:
                pass

        except ObjectDoesNotExist:

            return HttpResponseRedirect('/ciip/login/')

            
            
            
    return render(request, 'ciip/manager_home.html', {'user_name': user_name,'top_3':top_3,'results':results, 'previous_interviews_manager':previous_interviews_manager })



def schedule_interview(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username



        
        manager_profile = ManagerProfile.objects.get(user=request.user)
        email = User.objects.get(pk=current_pk).username
        student_id=request.GET['id']
        profile_student = UserProfile.objects.get(pk=student_id)
        university=profile_student.university
        date_info=return_best_time(university)
        current_time_there=date_info[0]
        suggested_time_frame=date_info[1]
        previous_interviews=Interview.objects.filter(student=profile_student)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/schedule_interview/')
        if request.method == 'POST' and len(Interview.objects.filter(manager=manager_profile)) <5:
            date=request.POST['day']
            skype_name=request.POST['skype_name']
            if len(skype_name)==0:
                skype_name='Webex scheduled through email'
            interview=Interview.objects.create(date=date, skype_name=skype_name,student=profile_student, manager=manager_profile)
            to_email=[profile_student.user.email]
            from_email=manager_profile.user.email
            subject='CIIP Application: Automatic Notification'
            message='Interview scheduled by manager '+manager_profile.first_name+' '+manager_profile.last_name+' at '+date+', Pacific Time. Please check your CIIP Profile for further informations. For any problem please email ciip_office@cisco.com'
            sendEmailNotification(from_email, to_email, subject, message)
            if profile_student.offer_states == 'Offered':
                pass
            else:
                profile_student.offer_states='Interviewing'
                profile_student.save()

          
            return HttpResponseRedirect('/ciip/manager_home')
       
            
    return render(request, 'ciip/schedule_interview.html', {'user_name': user_name,
                                             'profile_student':profile_student,
                                             'previous_interviews':previous_interviews,
                                             'previous_interviews_manager':previous_interviews_manager,
                                             'current_time_there':current_time_there,
                                             'suggested_time_frame':suggested_time_frame,
                                             'university':university})
  
def my_students(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        my_students_list =[]
        manager_profile = ManagerProfile.objects.get(user=request.user)
        email = User.objects.get(pk=current_pk).username
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/my_students/')
        for interview in previous_interviews_manager:
            if not interview.student in my_students_list:
                my_students_list.append(interview.student)
        try:
            student_id=request.GET['id']
            status=request.GET['status']
            student = UserProfile.objects.get(pk=student_id)
            match=re.search('Offered', student.offer_states)
            if not match:
                student.offer_states=status
                student.save()
            return HttpResponseRedirect('/ciip/my_students/')
        except MultiValueDictKeyError:
            pass

            
    return render(request, 'ciip/my_students.html', {'manager_profile':manager_profile,'user_name': user_name, 'my_students_list':my_students_list,'previous_interviews_manager':previous_interviews_manager})



def manager_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_info')

    return render(request, 'ciip/manager_info.html', {'user_name':user_name,'previous_interviews_manager':previous_interviews_manager ,'manager_profile':manager_profile})
    
def manager_edit_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_edit_info')

        if request.method=='POST':
            manager_profile.first_name=request.POST['first_name']
            manager_profile.last_name=request.POST['last_name']
            manager_profile.skill_1=request.POST['skill_1']
            manager_profile.skill_2=request.POST['skill_2']
            manager_profile.skill_3=request.POST['skill_3']
            manager_profile.interest_1=request.POST['interest_1']
            manager_profile.interest_2=request.POST['interest_2']
            manager_profile.interest_3=request.POST['interest_3']
            manager_profile.save()
            return HttpResponseRedirect('/ciip/manager_info/')
    return render(request, 'ciip/manager_edit_info.html', {'user_name':user_name, 'manager_profile':manager_profile, 'previous_interviews_manager':previous_interviews_manager})
def student_full_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user) 
        student_id=request.GET['id']
        student=UserProfile.objects.get(pk=student_id)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        interview_with_student=Interview.objects.filter(student=student, manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/student_full_profile')

        if request.method == 'POST':
            time =datetime.datetime.now()
            message=request.POST['message']+' posted by '+manager_profile.last_name+' at '+str(time)  
            student.manager_comment = message
            student.save()
            return HttpResponseRedirect('/ciip/student_full_profile?id='+str(student.id))
    return render(request, 'ciip/student_full_profile.html',{'previous_interviews_manager':previous_interviews_manager,'user_name':user_name,'student':student,'interview_with_student':interview_with_student})

def manager_send_message(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        to_email=[]
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_send_message')

        email = User.objects.get(pk=current_pk).username
        student_id=request.GET['id']
        student=UserProfile.objects.get(pk=student_id)
        student_email = student.user.email
        messages_sent=Message.objects.filter(manager=manager_profile,student=student).reverse()
        #a = range(len(messages_sent))
        #sorted(messages_sent, key=lambda x: a.index(x.date_sent))
        if request.method == 'POST':
            time =datetime.datetime.now()
            message=request.POST['message']
            message=Message.objects.create(text=message, manager=manager_profile, student=student, sent_by=manager_profile.first_name, date_sent=time)
            return HttpResponseRedirect('/ciip/manager_send_message/?id='+student_id)


       
            
    return render(request, 'ciip/manager_send_message.html', {'messages_sent':messages_sent,'user_name': user_name,'previous_interviews_manager':previous_interviews_manager})
def manager_logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/manager_login/') 
'''
def manager_signup(request):
    passcode='2860486313'
    if request.method == 'POST':
        form = SignUpFormManager(request.POST)
        
        if form.is_valid():
            email=request.POST['email']
            user_passcode = request.POST['passcode']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            business_unit=request.POST['business_unit']
            skill_1=request.POST['skill_1']
            skill_2=request.POST['skill_2']
            skill_3=request.POST['skill_3']
            interest_1=request.POST['interest_1']
            interest_2=request.POST['interest_2']
            interest_3=request.POST['interest_3']
            #import sys
            #print >> sys.stderr, "********* User Current PK %s" %(user_passcode)
            if checkciscoemail(email) and user_passcode==passcode:
                new_user = form.save()
                user=User.objects.get(email=email)
                ManagerProfile.objects.create(user=user,
                                              first_name=first_name,
                                              last_name=last_name,
                                              business_unit=business_unit,
                                              skill_1=skill_1,
                                              skill_2=skill_2,
                                              skill_3=skill_3,
                                              interest_1=interest_1,
                                              interest_2=interest_2,
                                              interest_3=interest_3
                    )

                return HttpResponseRedirect('/ciip/manager_login/')
            else:
                return HttpResponseRedirect('/ciip/manager_signup/')        
    else:
        form = SignUpFormManager()
        
    return render( request, 'ciip/manager_signup.html', {
        'form': form, 'passcode':passcode,
    })





def manager_login(request):
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/ciip/manager_home/')
            else:
                return HttpResponseRedirect('ciip/notactive/')
        else:
            return HttpResponseRedirect('/ciip/notregistered/')
    return render(request, 'ciip/manager_login.html', {'username':username, 'password':password})

def manager_home(request):
    results=[]
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        try:
            manager_profile = ManagerProfile.objects.get(user=request.user)
            previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
            #algorithm=functions()
            top_3=matchingAlgorith(manager_profile)
            delete_interview=request.GET.get('delete','')
            feedback=request.POST.get('feedback','')
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            if len(delete_interview) !=0:
                interview=Interview.objects.get(pk=delete_interview)
                interview.delete()
                return HttpResponseRedirect('/ciip/manager_home')

            try:
                query=request.GET['search']
                results=search_student(query)
                
            except MultiValueDictKeyError:
                pass
            try:
                filter_result=request.GET['sort']
                results=returnConfirmedOrNot(filter_result)
                
            except MultiValueDictKeyError:
                pass

        except ObjectDoesNotExist:

            return HttpResponseRedirect('/ciip/login/')

            
            
            
    return render(request, 'ciip/manager_home.html', {'user_name': user_name,'top_3':top_3,'results':results, 'previous_interviews_manager':previous_interviews_manager })



def schedule_interview(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username



        
        manager_profile = ManagerProfile.objects.get(user=request.user)
        email = User.objects.get(pk=current_pk).username
        student_id=request.GET['id']
        profile_student = UserProfile.objects.get(pk=student_id)
        university=profile_student.university
        date_info=return_best_time(university)
        current_time_there=date_info[0]
        suggested_time_frame=date_info[1]
        previous_interviews=Interview.objects.filter(student=profile_student)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        
        feedback=request.POST.get('feedback','')
        if len(feedback)!=0:
            sendFeedback(manager_profile, feedback)
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/schedule_interview/')
        if request.method == 'POST' and len(Interview.objects.filter(manager=manager_profile)) <5:
            skype_name=request.POST['skype_name']
            date=request.POST['day']
            if len(skype_name)==0:
                skype_name='Webex scheduled through email'
            interview=Interview.objects.create(date=date, skype_name=skype_name,student=profile_student, manager=manager_profile)
            to_email=[profile_student.user.email]
            from_email=manager_profile.user.email
            subject='CIIP Application: Automatic Notification'
            message='Interview scheduled by manager '+manager_profile.first_name+' '+manager_profile.last_name+' at '+date+', Pacific Time. Please check your CIIP Profile for further informations. For any problem please email ciip_office@cisco.com'
            sendEmailNotification(from_email, to_email, subject, message)
            match=re.search('Offered', profile_student.offer_states)
            if match:
                pass
            else:
                profile_student.offer_states='Interviewing'
                profile_student.save()
        
          
            return HttpResponseRedirect('/ciip/manager_home')
       
            
    return render(request, 'ciip/schedule_interview.html', {'user_name': user_name,
                                             'profile_student':profile_student,
                                             'previous_interviews':previous_interviews,
                                             'previous_interviews_manager':previous_interviews_manager,
                                             'current_time_there':current_time_there,
                                             'suggested_time_frame':suggested_time_frame,
                                             'university':university})
  
def my_students(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        my_students_list =[]
        manager_profile = ManagerProfile.objects.get(user=request.user)
        email = User.objects.get(pk=current_pk).username
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        feedback=request.POST.get('feedback','')
        if len(feedback)!=0:
            sendFeedback(manager_profile, feedback)
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/my_students/')
        for interview in previous_interviews_manager:
            if not interview.student in my_students_list:
                my_students_list.append(interview.student)
        try:
            student_id=request.GET['id']
            status=request.GET['status']
            student = UserProfile.objects.get(pk=student_id)
            match=re.search('Offered', student.offer_states)
            if not match:
                student.offer_states=status
                student.save()
            return HttpResponseRedirect('/ciip/my_students/')
        except MultiValueDictKeyError:
            pass

            
    return render(request, 'ciip/my_students.html', {'manager_profile':manager_profile,'user_name': user_name, 'my_students_list':my_students_list,'previous_interviews_manager':previous_interviews_manager})



def manager_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        feedback=request.POST.get('feedback','')
        if len(feedback)!=0:
            sendFeedback(manager_profile, feedback)
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_info')

    return render(request, 'ciip/manager_info.html', {'user_name':user_name,'previous_interviews_manager':previous_interviews_manager ,'manager_profile':manager_profile})
    
def manager_edit_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        
        
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_edit_info')

        if request.method=='POST':
            feedback=request.POST.get('feedback','')
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            manager_profile.first_name=request.POST['first_name']
            manager_profile.last_name=request.POST['last_name']
            manager_profile.business_unit=request.POST['business_unit']
            manager_profile.skill_1=request.POST['skill_1']
            manager_profile.skill_2=request.POST['skill_2']
            manager_profile.skill_3=request.POST['skill_3']
            manager_profile.interest_1=request.POST['interest_1']
            manager_profile.interest_2=request.POST['interest_2']
            manager_profile.interest_3=request.POST['interest_3']
            manager_profile.save()
            return HttpResponseRedirect('/ciip/manager_info/')
    return render(request, 'ciip/manager_edit_info.html', {'user_name':user_name, 'manager_profile':manager_profile, 'previous_interviews_manager':previous_interviews_manager})
def student_full_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user) 
        student_id=request.GET['id']
        student=UserProfile.objects.get(pk=student_id)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        interview_with_student=Interview.objects.filter(student=student, manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/student_full_profile')

        if request.method == 'POST':
            feedback=request.POST.get('feedback','')
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            time =datetime.now()
            message=request.POST['message']+' posted by '+manager_profile.last_name+' at '+str(time)  
            student.manager_comment = message
            student.save()
            return HttpResponseRedirect('/ciip/student_full_profile?id='+str(student.id))
    return render(request, 'ciip/student_full_profile.html',{'previous_interviews_manager':previous_interviews_manager,'user_name':user_name,'student':student,'interview_with_student':interview_with_student})

def manager_send_message(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        to_email=[]
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_send_message')

        email = User.objects.get(pk=current_pk).username
        student_id=request.GET['id']
        student=UserProfile.objects.get(pk=student_id)
        student_email = student.user.email
        messages_sent=Message.objects.filter(manager=manager_profile,student=student).reverse()
        #a = range(len(messages_sent))
        #sorted(messages_sent, key=lambda x: a.index(x.date_sent))
        if request.method == 'POST':
            feedback=request.POST.get('feedback','')
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            time =datetime.now()
            message=request.POST['message']
            message=Message.objects.create(text=message, manager=manager_profile, student=student, sent_by=manager_profile.first_name, date_sent=time)
            return HttpResponseRedirect('/ciip/manager_send_message/?id='+student_id)


       
            
    return render(request, 'ciip/manager_send_message.html', {'messages_sent':messages_sent,'user_name': user_name,'previous_interviews_manager':previous_interviews_manager, 'student':student})

def manager_guidelines(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else:
        current_pk = request.user.pk
        current_user = request.user
        user_name = User.objects.get(pk=current_pk).username
        manager_profile = ManagerProfile.objects.get(user=request.user)
        previous_interviews_manager=Interview.objects.filter(manager=manager_profile)
        delete_interview=request.GET.get('delete','')
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_guidelines')

    return render(request, 'ciip/manager_guidelines.html', {'user_name':user_name,'previous_interviews_manager':previous_interviews_manager ,'manager_profile':manager_profile})
 

def manager_logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/manager_login/') 