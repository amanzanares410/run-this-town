from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.views.generic import *
from django.db.models import Q

from mysite import settings
from django.conf import settings
import requests

from runningApp.models import Route


def index(request):
    return render(request=request, template_name="runningApp/index.html")

@login_required
def logged_in_view(request):
    # Check if the user's email is 'cs3240.super@gmail.com'
    routes = Route.objects.filter(Q(approved=True) | Q(user_id=request.user))
    route_start_points = []
    for r in routes:
        route_start_points.append([r.stops.first().latitude, r.stops.first().longitude]) # , r.route_name
    if request.user.email == 'cs3240.super@gmail.com':
        # Fetch the Admins group
        admin_group = Group.objects.get(name='Admins')
        # Add the user to the Admins group
        admin_group.user_set.add(request.user)
    if request.user.groups.filter(name='Admins').exists():
        # User is an admin
        return render(request=request, template_name="runningApp/logged_in_admin.html", context={"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY, "route_start_points": route_start_points })
    else:
        # User is a regular user
        return render(request=request, template_name="runningApp/logged_in.html", context={"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY, "route_start_points": route_start_points })

def logout_view(request):
    logout(request)
    return redirect('index')

# def map_view(request):
#     return render(request, template_name="runningApp/map.html")

def weather_view(request):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': 38.0293,
        'lon': -78.4767,
        'appid': settings.WEATHER_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(base_url, params=params)
    print(response.text)

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


class Route_View(ListView):
    template_name = 'runningApp/routes.html'
    model = Route
