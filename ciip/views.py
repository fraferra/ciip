# Create your views here.
import smtplib
import os
import re
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
from ciip.forms import  StatusUpdateForm  ,UserProfileForm , UploadFileForm, AcademicForm, MotivationalQuestionForm, SignUpForm, ImageForm, SkillForm, InterestForm
from django.http import HttpResponseRedirect, HttpResponse
from ciip.models import UserProfile
#from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required, permission_required



def signup(request):
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
        'form': form, 
    })


def login(request):
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
    return render(request, 'ciip/login.html', {'username':username, 'password':password})


def logout(request):
    django_logout(request)
    #eturn render(request, 'ciip/login.html')
    return HttpResponseRedirect('/ciip/login/')

def intern_profiles(request):
    return render(request, 'ciip/intern_profiles.html')

def notactive(request):
    if request.method =='POST':
        return HttpResponseRedirect('ciip/eligibility/')
    return render(request, 'ciip/notactive.html')

def notregistered(request):
    if request.method =='POST':
        return HttpResponseRedirect('/ciip/eligibility/')
    return render(request, 'ciip/notregistered.html')

def edit_contact_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method == 'POST':

            form = UserProfileForm(request.POST or None, instance=request.user.get_profile())
            #print("request user %s" % (request.user.id))
            # form.user_id = request.user.id
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/ciip/profile_contact_info/')
        else:
            form = UserProfileForm(instance = request.user.get_profile())
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
            
            profile = UserProfile.objects.get(pk=current_pk)
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


            contact_info={'user_name':user_name,'passport':passport ,'first_name':first_name,'last_name':last_name,
            'email':email,#'birth_date_day':birth_date_day,'birth_date_year':birth_date_year,'birth_date_month':birth_date_month,
            'gender':gender, 'address_line1':address_line1,
            'address_line2':address_line2, 'phone':phone,
            'city':city, 'zip_code':zip_code,
            'country':country, #'passport_number':passport_number,
            }
    return render(request, 'ciip/profile_contact_info.html', contact_info)




def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        status = UserProfile.objects.get(pk=current_pk).status 
        #if request.method =='GET':
            #profile = UserProfileForm(instance=request.user.get_profile())
            #user_name=str(profile['first_name'])
            #status_profile = StatusUpdateForm(instance=request.user.get_profile())
            #status=status_profile['status']
            
            
            
    return render(request, 'ciip/home.html', {'user_name': user_name,'status':status,})


def eligibility(request):
    return render(request,'ciip/eligibility.html')

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
            
            profile = UserProfile.objects.get(pk=current_pk)
            year_of_graduation= profile.year_of_graduation
            degree = profile.degree
            average= profile.average
            university = profile.university
            contact_info={'user_name':user_name, 'year_of_graduation':year_of_graduation,'degree':degree,'average':average,'university':university}
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



def motivational_questions(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:    
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username   
        if request.method == 'GET':
            
            profile = UserProfile.objects.get(pk=current_pk)
            question_1= profile.question_1
            question_2 = profile.question_2
            
            contact_info={'user_name':user_name,'question_1':question_1,'question_2':question_2}
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
            
            profile = UserProfile.objects.get(pk=current_pk)
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
    return render(request,'ciip/video.html')

def info(request):
    return render(request,'ciip/info.html')

def faq(request):
    return render(request,'ciip/faq.html')

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
                   send_mail(last_name+' '+ first_name, message, from_email , ['ciip.team.1@gmail.com'])
                   student_message='Dear '+first_name+', your request has been sent. Please wait until further notice from the CIIP Team. The process might take up to one week. Thank you!'
                   to_email=[email]
                   send_mail('message sent!', student_message, 'ciip.team.1@gmail.com', to_email)
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
    return render(request,'ciip/contact_us.html')


def forgot_password(request):
    email=''
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'ciip/forgot_password.html', {'email':email})




def checkemail(address):
    uni_list=['ucl.ac.uk','kent.ac.uk',
               'tsinghua.edu.cn',
               'zju.edu.cn','sfc.wide.ad.jp',
               'sfc.keio.ac.jp','unsw.edu.au',
               'student.bmstu.ru','fel.cvut.cz',
               'a2.keio.jp','a5.keio.jp','west.sd.keio.ac.jp',
               'ee.ucl.ac.uk', 'uottawa.ca',
               'epfl.ch','zju.edu.cn']
    match = re.search(r'([\w.-]+)@([\w.-]+)', address)
    for uni in uni_list:
        if match.group(2) == uni:
            return True
