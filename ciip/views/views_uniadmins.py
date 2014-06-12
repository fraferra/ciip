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
        
    return render( request, 'ciip/university/signup_uniadmin.html', {
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
    return render(request, 'ciip/university/uniadmin_login.html', {'username':username, 'password':password})





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



    return render(request, 'ciip/university/uniadmin_info.html', contact_info)


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


    return render( request, 'ciip/university/uniadmin_edit_info.html', {
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
            
            
            
    return render(request, 'ciip/university/home_uniadmin.html', {'user_name': user_name,})



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



    return render(request, 'ciip/university/list_student.html', {'university':university,'uni_list':uni_list, 'user_name':user_name, 'particular_student':particular_student})


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

    return render(request, 'ciip/university/student_info.html', {'user_name':user_name,
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
    return render( request, 'ciip/university/save_unicomment.html', {'form':form,  'user_name':user_name,
     'particular_student':particular_student, 'profile_student':profile_student})





    





