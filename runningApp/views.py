from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group



def index(request):
    return render(request=request, template_name="runningApp/index.html")

#@login_required
def logged_in_view(request):
      # Check if the user's email is 'cs3240.super@gmail.com'
    if request.user.email == 'cs3240.super@gmail.com':
        # Fetch the Admins group
        admin_group = Group.objects.get(name='Admins')
        # Add the user to the Admins group
        admin_group.user_set.add(request.user)
    if request.user.groups.filter(name='Admins').exists():
        # User is an admin
        return render(request=request, template_name="runningApp/logged_in_admin.html")
    else:
        # User is a regular user
        return render(request=request, template_name="runningApp/logged_in.html")

def logout_view(request):
    logout(request)
    return redirect('index')

def weather_view(request):
    return render(request, template_name="runningApp/weather.html")
