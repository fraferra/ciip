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

import pusher

class functions:
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
            match_field = re.search(str(obj_field).lower() ,str(student.suggested_position).lower())
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
                    match=re.search(str(obj_skill).lower(), str(student_skill).lower())
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
                    match=re.search(str(obj_interest).lower(), str(student_interest).lower())
                    if match:
                        score=score+0.7
            tmp_students_score.append((student, score))
        top_3=sorted(tmp_students_score,key=itemgetter(1))[-3:]
        top_3.reverse()
        return top_3
            

