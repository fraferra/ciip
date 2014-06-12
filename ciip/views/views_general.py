
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




def intern_profiles(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request, 'ciip/general/intern_profiles.html',{'user_name':user_name})

def notactive(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    if request.method =='POST':
        return HttpResponseRedirect('ciip/eligibility/')
    return render(request, 'ciip/general/notactive.html',{'user_name':user_name})

def notregistered(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    if request.method =='POST':
        return HttpResponseRedirect('/ciip/eligibility/')
    return render(request, 'ciip/general/notregistered.html',{'user_name':user_name})



def eligibility(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/general/eligibility.html',{'user_name':user_name})


def video(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/general/video.html', {'user_name':user_name})

def info(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/general/info.html', {'user_name':user_name})

def faq(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/general/faq.html',{'user_name':user_name})


def current_project(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request, 'ciip/general/current_project.html', {'user_name':user_name})




def contact_us(request):
    try:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
    except ObjectDoesNotExist:
        user_name='none'
    return render(request,'ciip/general/contact_us.html',{'user_name':user_name})


def forgot_password(request):
    email=''
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'ciip/general/forgot_password.html', {'email':email})

