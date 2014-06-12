# Create your views here.
import smtplib
import os
import re
from django.core.exceptions import *
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
from ciip.functions import *



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
        
    return render( request, 'ciip/student/signup.html', {
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
    return render(request, 'ciip/student/login.html', {'username':username, 'password':password,'user_name':user_name})


def logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/login/')

def profile_contact_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(user = request.user)
 
    return render(request, 'ciip/student/profile_contact_info.html', {'profile':profile})

def edit_contact_info(request):
    form=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        profile = UserProfile.objects.get(user = request.user)
        if profile.is_open is True:
            if request.method == 'POST':
                form = UserProfileForm(request.POST or None, instance=request.user.get_profile())
                #print("request user %s" % (request.user.id))
                # form.user_id = request.user.id
                if form.is_valid():
                    new_user = form.save()
                    return HttpResponseRedirect('/ciip/profile_contact_info/')
            else:
                form = UserProfileForm(instance=request.user.get_profile())
        else:
            return HttpResponseRedirect('/ciip/profile_contact_info/')
    return render( request, 'ciip/student/edit_contact_info.html', {
        'form': form, 'user_name':user_name,
    })




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
            
    return render(request, 'ciip/student/home.html', {'user_name': user_name,'status':status,})

def upload_file(request):
    form='Only accepted students will be able to upload the DS2019'
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        profile=UserProfile.objects.get(user=request.user)
        if profile.is_open is True:
            if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES, instance=request.user.get_profile())
                if form.is_valid():
                 # file is saved
                    new_user=form.save()
                    return HttpResponseRedirect('/ciip/upload_file/')
            else:
                form = UploadFileForm(instance=request.user.get_profile())
        else:
            form=profile.file_cv
    return render(request, 'ciip/student/upload_file.html', {'form': form,'user_name':user_name})



def upload_visa(request):
    form=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
       current_pk = request.user.pk
       user_name = User.objects.get(pk=current_pk).username
       student=UserProfile.objects.get(user=request.user)
       if student.status == 'Accepted':
           if request.method == 'POST':
               form = UploadVisaForm(request.POST, request.FILES, instance=request.user.get_profile())
               if form.is_valid():
                # file is saved
                   new_user=form.save()
                   sendEmailNotification('automated-reply@cisco.com', ['fraferra@cisco.com',], 'uploaded', 'ciao')
                   return HttpResponseRedirect('/ciip/upload_visa/')
           else:
               form = UploadVisaForm(instance=request.user.get_profile())
    return render(request, 'ciip/student/upload_visa.html', {'form': form,'user_name':user_name})




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
    return render(request, 'ciip/student/cover_letter.html', {'form': form,'user_name':user_name})





def send_email(request):
    return render(request,'ciip/general/contact_us.html')
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
    return render(request, 'ciip/student/academic_info.html', contact_info)



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
    return render( request, 'ciip/student/edit_academic_info.html', {
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
    return render(request, 'ciip/student/work_internship.html', contact_info)

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
    return render( request, 'ciip/student/edit_work_internship.html', {
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
    return render(request, 'ciip/student/motivational_questions.html', contact_info)


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
    return render( request, 'ciip/student/edit_motivational_questions.html', {
        'form': form, 'user_name':user_name,
    })




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
    return render( request, 'ciip/student/edit_skill_interest.html', {
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


    return render(request, 'ciip/student/skill_interest.html', skill_interest)



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
    return render(request,'/ciip/student/alternative_sign_up.html', {'university':university,
                                                    'first_name':first_name,
                                                    'last_name':last_name, 
                                                    'email':email,
                                                    })


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
            
    return render(request, 'ciip/student/interview.html', {'user_name':user_name, 'date_interview':date_interview,
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
    return render(request, 'ciip/student/my_managers.html', {'user_name':user_name, 'current_student':current_student,'interviews_with_managers':interviews_with_managers})

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
            from_email=current_student.user.email
            to_email=[current_manager.user.email]
            subject='Student '+current_student.first_name+' '+current_student.last_name+' sent a message on CIIP.'
            message='Check https://www.ciip4me.com/ciip/manager_send_message?id='+str(current_student.id)
            sendEmailNotification(from_email, to_email, subject, message)
            return HttpResponseRedirect('/ciip/student_send_message/?id='+manager_id)

    return render(request, 'ciip/student/student_send_message.html', {'user_name':user_name, 'previous_messages':previous_messages})











