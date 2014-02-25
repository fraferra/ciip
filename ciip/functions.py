from operator import itemgetter
# Create your views here.
import smtplib
import os
from datetime import datetime
import re
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
from ciip.forms import * #StatusUpdateForm  ,UserProfileForm , EndorsementForm, UnicommentForm, SignUpFormAdmin, UniAdminForm , WorkForm, CoverForm, UploadFileForm, AcademicForm, MotivationalQuestionForm, SignUpForm,  SkillForm, InterestForm
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



class functions:
    def matchingAlgorith(self,obj):
        obj_skills=[obj.skill_1, obj.skill_2, obj.skill_3]
        obj_field=obj.business_unit
        field=''
        technical_fields=['Technology radar','SDN / Engineering',
                          'Openstack / Engineering','IT',
                          'GIS / IT','Collaboration / IT',
                          'Security / Engineering',
                          'Engineering',
                          'Cloud / Engineering','CIIP Tools / Engineering',
                          'CSMTG / Engineering','ONE PK / Engineering']
        business_fields=['Marketing','Sales']
        if obj_field in technical_fields:
            field='technical'
        if obj_field in business_fields:
            field='business'
        obj_interests=[obj.interest_1, obj.interest_2, obj.interest_3]
        obj_alls=obj_skills+obj_interests
        top_3=[]
        tmp_students_score=[]
        max_score=0
        for student in UserProfile.objects.all():
            score=0
            match_field = re.search(str(obj_field).lower() ,str(student.position_suggested).lower())
            if match_field:
                score=score+3
            for skill in obj_skills:
                match=re.search(unicode(student.degree).lower(), unicode(skill).lower())
                if match:
                    score=score+1
            #student_business_fields=['management', 'business', 'marketing']
            #student_technical_fields=['engineering', 'electrical', 'computer science', 'big data','electronic', 'cs']

            #check_degree=re.search()
            interview_fields=[student.leadership, student.initiative, student.innovation, 
                              student.adaptability, student.team_player, student.cisco_fit,
                              student.technical_skill, student.motivation ]
            for interview_field in interview_fields:
                if interview_field == 'Yes':
                    score=score+0.2
            #match_uni_field=re.findall(field, unicode(student.uni_comment))
            #score=score+0.2*len(match_uni_field)
            if student.university_endorsement == 'Strongly recommended':
                score=score+0.5
            if student.university_endorsement == 'Recommended':
                score=score+0.2
            student_skills=[(student.skill_1,student.skill_level_1),(student.skill_2, student.skill_level_2),(student.skill_3,student.skill_level_3)]
            student_interests=[student.interest_1, student.interest_2, student.interest_3]
            for student_skill, student_level in student_skills:
                for obj_skill in obj_alls:
                    match=re.search(unicode(obj_skill).lower(), unicode(student_skill).lower())
                    if match:
                        if student_level == 'Advanced':
                            score=2+score
                        if student_level == 'Intermediate':
                            score=1.5+score
                        if student_level == 'Beginner':
                            score=1+score
            for student_interest in student_interests:
               for obj_interest in obj_alls:
                    match=re.search(unicode(obj_interest).lower(), unicode(student_interest).lower())
                    if match:
                        score=score+0.7
            tmp_students_score.append((student, score))
        top_3=sorted(tmp_students_score,key=itemgetter(1))[-3:]
        top_3.reverse()
        return top_3
        '''
    def matchingAlgorith(self,obj):
        obj_skills=[obj.skill_1, obj.skill_2, obj.skill_3]
        obj_field=obj.business_unit
        field=''
        technical_fields=['network','data center','engineering','gis','it']
        business_fields=['marketing','sales','digital marketing']
        if obj_field in technical_fields:
            field='technical'
        if obj_field in business_fields:
            field='business'
        obj_interests=[obj.interest_1, obj.interest_2, obj.interest_3]
        obj_alls=obj_skills+obj_interests
        top_3=[]
        tmp_students_score=[]
        max_score=0
        for student in UserProfile.objects.all():
            score=0
            match_field = re.search(unicode(obj_field).lower() ,unicode(student.position_suggested).lower())
            if match_field:
                score=score+3
            for skill in obj_skills:
                match=re.search(unicode(student.degree).lower(), unicode(skill).lower())
                if match:
                    score=score+1
            student_skills=[(student.skill_1,student.skill_level_1),(student.skill_2, student.skill_level_2),(student.skill_3,student.skill_level_3)]
            student_interests=[student.interest_1, student.interest_2, student.interest_3]
            for student_skill, student_level in student_skills:
                for obj_skill in obj_alls:
                    match=re.search(unicode(obj_skill).lower(), unicode(student_skill).lower())
                    if match:
                        if student_level == 'Advanced':
                            score=2+score
                        if student_level == 'Intermediate':
                            score=1.5+score
                        if student_level == 'Beginner':
                            score=1+score
                        #score=score+1
            for student_interest in student_interests:
               for obj_interest in obj_alls:
                    match=re.search(unicode(obj_interest).lower(), unicode(student_interest).lower())
                    if match:
                        score=score+0.7
            tmp_students_score.append((student, score))
        top_3=sorted(tmp_students_score,key=itemgetter(1))[-3:]
        top_3.reverse()
        return top_3
            '''
def matchingAlgorith(obj):
    obj_skills=[obj.skill_1, obj.skill_2, obj.skill_3]
    obj_field=obj.business_unit
    field=''
    technical_fields=['Technology radar','SDN / Engineering',
                          'Openstack / Engineering','IT',
                          'GIS / IT','Collaboration / IT',
                          'Security / Engineering',
                          'Engineering',
                          'Cloud / Engineering','CIIP Tools / Engineering',
                          'CSMTG / Engineering','ONE PK / Engineering']
    business_fields=['Marketing','Sales']
    if obj_field in technical_fields:
        field='technical'
    if obj_field in business_fields:
        field='business'
    obj_interests=[obj.interest_1, obj.interest_2, obj.interest_3]
    obj_alls=obj_skills+obj_interests
    top_3=[]
    tmp_students_score=[]
    max_score=0
    for student in UserProfile.objects.all():
        score=0
        match_field = re.search(str(obj_field).lower() ,str(student.position_suggested).lower())
        if match_field:
            score=score+3
        for skill in obj_skills:
            match=re.search(unicode(student.degree).lower(), unicode(skill).lower())
            if match:
                score=score+1
            #student_business_fields=['management', 'business', 'marketing']
            #student_technical_fields=['engineering', 'electrical', 'computer science', 'big data','electronic', 'cs']

            #check_degree=re.search()
        interview_fields=[student.leadership, student.initiative, student.innovation, 
                              student.adaptability, student.team_player, student.cisco_fit,
                              student.technical_skill, student.motivation ]
        for interview_field in interview_fields:
            if interview_field == 'Yes':
                    score=score+0.2
            #match_uni_field=re.findall(field, unicode(student.uni_comment))
            #score=score+0.2*len(match_uni_field)
        if student.university_endorsement == 'Strongly recommended':
            score=score+0.5
        if student.university_endorsement == 'Recommended':
            score=score+0.2
        student_skills=[(student.skill_1,student.skill_level_1),(student.skill_2, student.skill_level_2),(student.skill_3,student.skill_level_3)]
        student_interests=[student.interest_1, student.interest_2, student.interest_3]
        for student_skill, student_level in student_skills:
            for obj_skill in obj_alls:
                match=re.search(unicode(obj_skill).lower(), unicode(student_skill).lower())
                if match:
                    if student_level == 'Advanced':
                        score=2+score
                    if student_level == 'Intermediate':
                        score=1.5+score
                    if student_level == 'Beginner':
                        score=1+score
        for student_interest in student_interests:
            for obj_interest in obj_alls:
                match=re.search(unicode(obj_interest).lower(), unicode(student_interest).lower())
                if match:
                    score=score+0.7
        tmp_students_score.append((student, score))
    top_3=sorted(tmp_students_score,key=itemgetter(1))[-3:]
    top_3.reverse()
    return top_3


def sendEmailNotification(from_email, to_email, subject, message):
    try:
        send_mail(subject, message, from_email , to_email)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def search_student(search, sortby):
    results=[]
    if len(sortby)=0:
        list_students=UserProfile.objects.all()
    else:
        list_students=UserProfile.objects.filter(offer_states=sortby)
    for user in list_students:
        fields = [user.skill_1, user.skill_2, user.skill_3,
                  user.degree, user.first_name, user.last_name,
                   user.university, user.position_suggested, user.interest_1,
                    user.interest_2,user.interest_3]
        for value in fields:
            if value is not None:
                match = re.search(search.lower(), value.lower())
                if match:
                    if user not in results:
                        results.append(user)
    return results     
        
def returnConfirmedOrNot(filter_result):
    results=[] 
    if filter_result == 'rejected':
        results=UserProfile.objects.filter(offer_states='Rejected')
        #for user in UserProfile.objects.all():
           #if user.offer_states == 'Rejected':
                #results.append(user)
    if filter_result == 'not_offered_yet':
        for user in UserProfile.objects.all():
            if user.offer_states is None:
                results.append(user)
    if filter_result == 'interviewing':
        for user in UserProfile.objects.all():
            if user.offer_states == 'Interviewing':
                results.append(user)
    if filter_result == 'accepted':
        for user in UserProfile.objects.all():
            match=re.search('Offered', str(user.offer_states))
            if match:
                results.append(user)       
    return results


def return_best_time(university):
    local_tz=timezone('US/Pacific')
    #time = local_tz.localize(datetime.datetime.now())
    time = local_tz.localize(datetime.now())
    if university == 'UCL' or university=='Kent':
        tz= timezone('Europe/London')
        suggested_time_frame= university +" is currently 8 hours ahead. The best time suggested to schedule an interview is between 8am and 10am, Pacific Time."
    if university == 'ZJU' or university == 'Tsinghua':
        tz= timezone('Asia/Shanghai')
        suggested_time_frame= university +" is currently 16 hours ahead. The best time suggested to schedule an interview is between 4pm and 6pm, Pacific Time."
    if university == 'Keio':
        tz= timezone("Japan")
        suggested_time_frame= university +" is currently 17 hours ahead. The best time suggested to schedule an interview is between 5pm and 6pm, Pacific Time."
    if university == 'BMSTU':
        tz= timezone("Europe/Moscow")
        suggested_time_frame= university +" is currently 12 hours ahead. The best time suggested to schedule an interview is between 8am and 10am, Pacific Time."
    #current_time=datetime.datetime.now(tz)
    #current_time=timezone.localtime(tz)
    fmt = '%Y-%m-%d %H:%M'
    current_time = tz.normalize(time.astimezone(tz)).strftime(fmt)
    date_info=[current_time, suggested_time_frame]
    return date_info

def getUniAdmin(email, current_user):
    match = re.search(r'([\w.-]+)@([\w.-]+)', email)
    newemail = match.group(2).replace (".", " ")
    profile = UniversityAdmin.objects.get(user=current_user)
    uni = newemail.split()
    for word in uni:
        if word == 'ucl':
            #uni_origin = University.objects.get(name='UCL')
            profile.university = 'UCL'
            profile.save()
        if word == 'kent':
            #uni_origin = University.objects.get(name='Kent')
            profile.university = 'Kent'
            profile.save()
        if word == 'tsinghua':
            #uni_origin = University.objects.get(name='Tsinghua')
            profile.university = 'Tsinghua'
            profile.save()
        if word == 'zju':
            #uni_origin = University.objects.get(name='ZJU')
            profile.university = 'ZJU'
            profile.save()
        if word == 'wide' or word == 'keio':
            #uni_origin = University.objects.get(name='Keio')
            profile.university = 'Keio'
            profile.save()
        if word == 'cvut':
            #uni_origin = University.objects.get(name='CTU')
            profile.university = '  CTU'
            profile.save()
        if word == 'bmstu':
            #uni_origin = University.objects.get(name='BMSTU')
            profile.university = 'BMSTU'
            profile.save()
        if word == 'epfl':
            #uni_origin = University.objects.get(name='EPFL')
            profile.university = 'EPFL'
            profile.save()
        if word == 'unsw':
            #uni_origin = University.objects.get(name='UNSW')
            profile.university = 'UNSW'
            profile.save()


def checkemail(address):
    uni_list=['ucl.ac.uk','kent.ac.uk',
               'tsinghua.edu.cn',
               'zju.edu.cn','sfc.wide.ad.jp',
               'sfc.keio.ac.jp','unsw.edu.au',
               'student.bmstu.ru','fel.cvut.cz',
               'a2.keio.jp','a5.keio.jp','west.sd.keio.ac.jp',
               'z5.keio.jp','bmstu.ru',
               'ee.ucl.ac.uk', 'uottawa.ca',
               'epfl.ch','zju.edu.cn']
    match = re.search(r'([\w.-]+)@([\w.-]+)', address)
    for uni in uni_list:
        if match.group(2) == uni:
            return True

def checkciscoemail(address):
    cisco_email='cisco.com'
    match = re.search(r'([\w.-]+)@([\w.-]+)', address)
    if match.group(2) == cisco_email:
        return True

def sendFeedback(manager, feedback):
    to_email=['fraferra@cisco.com','elbowen@cisco.com']
    from_email=manager.user.email
    message=feedback
    subject='Feedback from Manager '+manager.last_name+'. Email:'+manager.user.email
    sendEmailNotification(from_email, to_email, subject, message)
    feedback=''