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
            coordinator=request.POST['coordinator']
            #import sys
            #print >> sys.stderr, "********* User Current PK %s" %(user_passcode)
            if checkciscoemail(email) and user_passcode==passcode:
                new_user = form.save()
                user=User.objects.get(email=email)
                ManagerProfile.objects.create(user=user,
                                              coordinator=coordinator,
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
        
    return render( request, 'ciip/manager/manager_signup.html', {
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
                return HttpResponseRedirect('ciip/manager_login/')
        else:
            return HttpResponseRedirect('/ciip/manager_login/')
    return render(request, 'ciip/manager/manager_login.html', {'username':username, 'password':password})

def manager_home(request):
    results=[]
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/manager_login/')
    else: 
        number_results=0
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
                offer_status=request.GET['offer_status']
                query=request.GET['search']

                ranking=request.GET['ranking']
                university=request.GET['university']
                results=search_student(query, offer_status, ranking, university)
                number_results=len(results)
                time =datetime.now()
                Search.objects.create(manager=manager_profile,date=time, search=query, university=university, ranking=ranking, offer_status=offer_status)
            except MultiValueDictKeyError:
                pass
            try:
                filter_result=request.GET['sort']
                results=returnConfirmedOrNot(filter_result)
                
            except MultiValueDictKeyError:
                pass

        except ObjectDoesNotExist:

            return HttpResponseRedirect('/ciip/login/')

            
            
            
    return render(request, 'ciip/manager/manager_home.html', {'manager_profile':manager_profile,
                                                      'user_name': user_name,'top_3':top_3,
                                                      'results':results, 
                                                      'previous_interviews_manager':previous_interviews_manager,
                                                      'number_results':number_results })

def manager_history(request):
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
            delete_search=request.GET.get('delete2','')
            feedback=request.POST.get('feedback','')
            delete_all=request.GET.get('delete_all','')
            if delete_all=='delete_all':
                for se in Search.objects.filter(manager=manager_profile):
                    se.delete()
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            if len(delete_interview) !=0:
                interview=Interview.objects.get(pk=delete_interview)
                interview.delete()
                return HttpResponseRedirect('/ciip/manager_history')
            if len(delete_search) !=0:
                search=Search.objects.get(pk=delete_search)
                search.delete()
            previous_search=Search.objects.filter(manager=manager_profile)
        except ObjectDoesNotExist:

            return HttpResponseRedirect('/ciip/login/')                   
    return render(request, 'ciip/manager/manager_history.html', {'user_name': user_name,'previous_search':previous_search,
                                                           'previous_interviews_manager':previous_interviews_manager})
 



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
            return HttpResponseRedirect('/ciip/schedule_interview/?id='+student_id)
        coordinator=request.GET.get('coordinator','')
        coordinator_id=request.GET.get('coordinator_id','')
        business_unit_coordinators=ManagerProfile.objects.filter(coordinator='yes', business_unit=manager_profile.business_unit)
        if coordinator=='yes':
            current_coordinator=ManagerProfile.objects.get(pk=coordinator_id)
            Interview.objects.create(student=profile_student, manager=manager_profile, delegated_to=current_coordinator)
            to_email=[current_coordinator.user.email]
            from_email=manager_profile.user.email
            subject='CIIP Application: '+manager_profile.first_name+ ' '+manager_profile.last_name +' delegated you for an interview.'
            message='Manager '+manager_profile.first_name+' '+manager_profile.last_name+' would like you schedule an interview with '+profile_student.last_name+'. Please check www.ciip4me.com/ciip/manager_home/ for further informations. For any problem please email ciip_office@cisco.com'
            sendEmailNotification(from_email, to_email, subject, message)
            return HttpResponseRedirect('/ciip/schedule_interview/?id='+student_id)
        else:
            if request.method == 'POST' and len(Interview.objects.filter(manager=manager_profile)) <5:
                skype_name=request.POST.get('skype_name','')
                try:
                    date=request.POST.get('day')
                    if len(skype_name)==0:
                        skype_name='Webex scheduled through email'
                    interview=Interview.objects.create(date=date, skype_name=skype_name,student=profile_student, manager=manager_profile)
                    to_email=[profile_student.user.email]
                    from_email=manager_profile.user.email
                    subject='CIIP Application: Automatic Notification'
                    message='Interview scheduled by manager '+manager_profile.first_name+' '+manager_profile.last_name+' at '+date+', Pacific Time. Please check your CIIP Profile for further informations. For any problem please email ciip_office@cisco.com'
                    sendEmailNotification(from_email, to_email, subject, message)
                except ValidationError:
                    return HttpResponseRedirect('/ciip/schedule_interview/?id='+student_id)
                #if len(skype_name)==0:
                    #skype_name='Webex scheduled through email'
                #interview=Interview.objects.create(date=date, skype_name=skype_name,student=profile_student, manager=manager_profile)
                if type(profile_student.offer_states) is str:
                    match=re.search('Offered', profile_student.offer_states)
                    if match:
                        pass
                    else:
                        profile_student.offer_states='Interviewing'
                        profile_student.save()
            
              
                return HttpResponseRedirect('/ciip/manager_home')
           
            
    return render(request, 'ciip/manager/schedule_interview.html', {'user_name': user_name,
                                             'business_unit_coordinators':business_unit_coordinators,
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
        interviews_delegated=[]
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
        if manager_profile.coordinator=='yes':
            interviews_delegated=Interview.objects.filter(delegated_to=manager_profile)

        for interview in previous_interviews_manager:
            if not interview.student in my_students_list:
                my_students_list.append(interview.student)
        try:
            student_id=request.GET['id']
            status=request.GET['status']
            student = UserProfile.objects.get(pk=student_id)
            match=re.search('offer', str(student.offer_states).lower())
            if not match:
                student.offer_states=status
                student.save()
            return HttpResponseRedirect('/ciip/my_students/')
        except MultiValueDictKeyError:
            pass

            
    return render(request, 'ciip/manager/my_students.html', {'manager_profile':manager_profile,
        'user_name': user_name,
         'my_students_list':my_students_list,
         'interviews_delegated':interviews_delegated,
         'previous_interviews_manager':previous_interviews_manager})



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

    return render(request, 'ciip/manager/manager_info.html', {'user_name':user_name,'previous_interviews_manager':previous_interviews_manager ,'manager_profile':manager_profile})
    
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
            manager_profile.first_name=request.POST.get('first_name','')
            manager_profile.last_name=request.POST.get('last_name','')
            manager_profile.business_unit=request.POST.get('business_unit','')
            manager_profile.skill_1=request.POST.get('skill_1','')
            manager_profile.skill_2=request.POST.get('skill_2','')
            manager_profile.skill_3=request.POST.get('skill_3','')
            manager_profile.interest_1=request.POST.get('interest_1','')
            manager_profile.interest_2=request.POST.get('interest_2','')
            manager_profile.interest_3=request.POST.get('interest_3','')
            manager_profile.coordinator=request.POST.get('coordinator','')
            manager_profile.work_description=request.POST.get('work_description','')
            
            #manager_profile.job_title=request.POST.get('job_title','')
           # manager_profile.degree=request.POST.get('degree','')
           # manager_profile.field=request.POST.get('field','')
           # manager_profile.group=request.POST.get('group','')
           # manager_profile.year_experience=request.POST.get('year_experience','')

            manager_profile.vap=request.POST.get('vap')
            manager_profile.number_interns=request.POST.get('number_interns')
            form = ds7002Form(request.POST, request.FILES, instance=manager_profile)
            manager_profile.save()
            
            if form.is_valid():
            # file is saved
               new_user=form.save()
            return HttpResponseRedirect('/ciip/manager_info/') 
        else:
            form = ds7002Form(instance=manager_profile)      
            
    return render(request, 'ciip/manager/manager_edit_info.html', {'user_name':user_name,
                                                          'manager_profile':manager_profile, 
                                                          'previous_interviews_manager':previous_interviews_manager,
                                                          'form':form})



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
            message=request.POST.get('message','')
            if len(message)!=0:
                message=message+' posted by '+manager_profile.last_name+' at '+str(time)+'\n'  
                student.manager_comment = message
                student.save()
            return HttpResponseRedirect('/ciip/student_full_profile?id='+str(student.id))
    return render(request, 'ciip/manager/student_full_profile.html',{'previous_interviews_manager':previous_interviews_manager,'user_name':user_name,'student':student,'interview_with_student':interview_with_student})

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
        student_id=request.GET['id']
        student=UserProfile.objects.get(pk=student_id)
        if len(delete_interview) !=0:
            interview=Interview.objects.get(pk=delete_interview)
            interview.delete()
            return HttpResponseRedirect('/ciip/manager_send_message?id='+student_id)

        email = User.objects.get(pk=current_pk).username
        
        
        student_email = student.user.email
        messages_sent=Message.objects.filter(manager=manager_profile,student=student).reverse()
        #a = range(len(messages_sent))
        #sorted(messages_sent, key=lambda x: a.index(x.date_sent))
        if request.method == 'POST':
            feedback=request.POST.get('feedback','')
            if len(feedback)!=0:
                sendFeedback(manager_profile, feedback)
            time =datetime.now()
            message=request.POST.get('message','')
            if len(message)!=0:
                message=Message.objects.create(text=message, manager=manager_profile, student=student, sent_by=manager_profile.first_name, date_sent=time)
                from_email=manager_profile.user.email
                to_email=[student_email]
                subject='Manger '+manager_profile.first_name+' '+manager_profile.last_name+' sent a message on CIIP.'
                message='Check https://www.ciip4me.com/ciip/student_send_message?id='+str(manager_profile.id)
                sendEmailNotification(from_email, to_email, subject, message)
            return HttpResponseRedirect('/ciip/manager_send_message/?id='+student_id)


       
            
    return render(request, 'ciip/manager/manager_send_message.html', {'messages_sent':messages_sent,'user_name': user_name,'previous_interviews_manager':previous_interviews_manager, 'student':student})

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

    return render(request, 'ciip/manager/manager_guidelines.html', {'user_name':user_name,'previous_interviews_manager':previous_interviews_manager ,'manager_profile':manager_profile})
 

def manager_logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/manager_login/') 

import boto
import os
from boto.s3.connection import S3Connection

from django.conf import settings

# "https://s3-us-west-2.amazonaws.com/ciip.media/media/{{student.file_cv}}
def downloads(request):

    import logging
    logger = logging.getLogger(__name__)

    filename = request.GET.get('file')
    s3_filename = "media/%s" % (filename)
    short_filename = os.path.basename(filename)

    conn = S3Connection("AKIAJD2OM3MYDTC2BFRQ", "Re+FENQuiKKPKLmoyr03gomVzp6lT05CibIPuktb")
   
    bucket_name = ""
    if settings.DEBUG == True:
        bucket_name = "ciip.dev.media"
    else:
        bucket_name = "ciip.media"

    bucket = conn.get_bucket(bucket_name)
    
    key = bucket.get_key(s3_filename)
    content = key.get_contents_as_string()

    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition']='attachment;filename="%s"'%short_filename
    response["X-Sendfile"] = short_filename
    response.write(content)

    return response