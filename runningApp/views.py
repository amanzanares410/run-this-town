from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.conf import settings
import requests


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
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': 'Charlottesville, VA',
        'appid': settings.WEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        context = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    else:
        context = {
            'error': 'Unable to fetch weather data for Charlottesville, VA.'
        }

    return render(request, 'runningApp/weather.html', context)
