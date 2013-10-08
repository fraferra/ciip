# Create your views here.

from django.shortcuts import render, render_to_response
#from ciip.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
#from ciip.models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
           new_user = form.save()
           return HttpResponseRedirect('/ciip/signup/')
    else:
        form = UserCreationForm()
    return render( request, 'ciip/signup.html', {
        'form': form,
    })



def login(request):
    username=password=''
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/ciip/profile/')
            else:
                return HttpResponseRedirect('/ciip/error/')
        else:
            return HttpResponseRedirect('/ciip/lol/')
    return render(request, 'ciip/login.html', {'username':username, 'password':password})


