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


