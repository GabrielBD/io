from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages

from django.contrib.auth import authenticate, login as login_mio, logout as logout_mio
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required



# Create your views here.
def login(request):
    titulo 	= 'Login'
    template = loader.get_template('auth2/login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_mio(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Error en password o usuario')
    context = {
    'titulo': titulo,
    }
    return HttpResponse(template.render(context, request))


def register(request):
    titulo 	= 'Register'
    template = loader.get_template('auth2/register.html')
    if request.method == "POST":
        username 	= request.POST['username']
        email 		= request.POST['email']
        password 	= request.POST['password']
                
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, 'Registro completo, ahora puede loguearse.')
            return redirect('login')
        else:
            messages.error(request, 'Nombre de usuario duplicado.')

    context = {
        'titulo': titulo,
    }

    return HttpResponse(template.render(context, request))


@login_required
def edit(request):
    titulo  = 'Editar Datos de Usuario'
    template = loader.get_template('auth2/useredit.html')
    
    user_username   = request.user.username
    user_email      = request.user.email

    if request.method == "POST":
        username    = request.POST['username']
        email       = request.POST['email']
                
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            request.user.username = username 
            request.user.email = email
            request.user.save()
            messages.success(request, 'Éxito al editar el usuario.')
            return redirect('modelo1_index')
        else:
            messages.error(request, 'Nombre de usuario duplicado.')

    context = {
        'titulo': titulo,
        'user_username'     : user_username,
        'user_email'        : user_email
    }

    return HttpResponse(template.render(context, request))



def logout(request):
    logout_mio(request)
    return redirect('login')