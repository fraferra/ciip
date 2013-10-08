# Create your views here.

from django.shortcuts import render, render_to_response, redirect
from ciip.forms import UserProfileForm, StatusUpdateForm, UploadFileForm#, UserCreationForm
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
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            
            new_user = form.save()   

            return HttpResponseRedirect('/ciip/login/')
    else:
        form = UserCreationForm()
        
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



def notactive(request):
    if request.method =='POST':
        return HttpResponseRedirect('ciip/signup/')
    return render(request, 'ciip/notactive.html')

def notregistered(request):
    if request.method =='POST':
        return HttpResponseRedirect('/ciip/signup/')
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
            
        if request.method == 'GET':
            current_pk = request.user.pk
            user_name = User.objects.get(pk=current_pk).username
            profile = UserProfile.objects.get(pk=current_pk)
            first_name= profile.first_name
            last_name = profile.last_name
            email= profile.email
            university = profile.university
            contact_info={'user_name':user_name, 'first_name':first_name,'last_name':last_name,'email':email,'university':university}
    return render(request, 'ciip/profile_contact_info.html', contact_info)




def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else: 
        if request.method =='GET':
            #profile = UserProfileForm(instance=request.user.get_profile())
            #user_name=str(profile['first_name'])
            #status_profile = StatusUpdateForm(instance=request.user.get_profile())
            #status=status_profile['status']
            current_pk = request.user.pk
            
            user_name = User.objects.get(pk=current_pk).username
            
            status = UserProfile.objects.get(pk=current_pk).status
    return render(request, 'ciip/home.html', {'user_name': user_name,'status':status,})


def eligibility(request):
    return render(request,'ciip/eligibility.html')



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
                form.save()
                return HttpResponseRedirect('/ciip/home/')
        else:
            form = UploadFileForm(instance = request.user.get_profile()).file_cv
    return render(request, 'ciip/upload_file.html', {'form': form, 'user_name':user_name})


def upload_file(request):
    current_pk = request.user.pk
    user_name = User.objects.get(pk=current_pk).username
    p = UserProfile.objects.get(pk=current_pk)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        user=UserProfile
        if request.method == 'POST':
            #u=UserProfile.objects.get(pk=current_pk)
            new_file = UserProfile(user=request.user)
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                
                
            # file is saved
                #instance = UserProfile(user_id=current_pk)
                #u.file_cv=request.FILES['file'].save()
                instance = UserProfile(file_cv=request.FILES['file'])
                instance.save(force_insert=True)
                return HttpResponseRedirect('/ciip/home/')
        else:
            form = UploadFileForm()
    return render(request, 'ciip/upload_file.html', {'form': form, 'user_name':user_name,})


def upload_file(request):
    current_pk = request.user.pk
    user_name = User.objects.get(pk=current_pk).username
    p = UserProfile.objects.get(pk=current_pk)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')

    else:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

   def change_password(request):
    new_password=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
        if request.method=='POST':

           u = User.objects.get(username__exact=user_name)
           new_password = request.POST['new_password']
           u.set_password(new_password)
           u.save() 
           return HttpResponseRedirect('/ciip/home/')
    return render(request, 'ciip/change_password.html', {'user_name': user_name, 'new_password':new_password,})'''





'''def password_change(request,
                    template_name='/ciip/change_password.html',
                    post_change_redirect='/ciip/home/',
                    password_change_form=ChangePassword,
                    current_app='ciip',
                     ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/ciip/login/')
    else:
        current_pk = request.user.pk
        user_name = User.objects.get(pk=current_pk).username
         
        if request.method == 'POST':
            form = ChangePassword(request.POST)
            if form.is_valid():
                form.save()
        else:
            form=ChangePassword(instance=request.user)

    return render(request, 'ciip/change_password.html',{'form':form,'user_name':user_name,} )'''

