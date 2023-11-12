from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.views.generic import *
from django.db.models import Q

from mysite import settings
from django.conf import settings
import requests
import json

from runningApp.models import Route, Stop, RouteStop


def index(request):
    return render(request=request, template_name="runningApp/index.html")

@login_required
def logged_in_view(request):
    # Check if the user's email is 'cs3240.super@gmail.com'
    routes = Route.objects.filter(Q(approved=True) | Q(user_id=request.user))
    route_start_points = []
    for r in routes:
        route_start_points.append([r.stops.first().latitude, r.stops.first().longitude, r.id, r.distance, r.gradient_range]) # , r.route_name
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

def create_route(request):
    return render(request=request, template_name="runningApp/create_route.html", context={"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY})

# def map_view(request):
#     return render(request, template_name="runningApp/map.html")
@login_required
def weather_view(request):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': 38.0293,
        'lon': -78.4767,
        'appid': settings.WEATHER_API_KEY,
        'units': 'imperial'
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

def social(request):
    query = request.GET.get('friend-search')
    if query:
        users = User.objects.filter(email__icontains=query).prefetch_related('route_set')
    else:
        users = User.objects.none()
    return render(request=request, template_name="runningApp/social.html", context={'users': users})


class Route_View(LoginRequiredMixin, ListView):
    template_name = 'runningApp/routes.html'
    model = Route


class Route_Detail(LoginRequiredMixin, DetailView):
    model = Route

    def get_template_names(self):
        if self.request.user.groups.filter(name='Admins').exists():
            return ['runningApp/logged_in_admin.html']
        else:
            return ['runningApp/logged_in.html']

    def get_context_data(self, **kwargs):
        route_id = self.kwargs['pk']
        current_stops = Route.objects.get(id=route_id).stops.all().order_by('routestop__stop_order')

        routes = Route.objects.filter(Q(approved=True) | Q(user_id=self.request.user))
        route_start_points = []
        for r in routes:
            route_start_points.append([r.stops.first().latitude, r.stops.first().longitude, r.id]) # , r.route_name
        context = super().get_context_data(**kwargs)
        context["GOOGLE_MAPS_API_KEY"] = settings.GOOGLE_MAPS_API_KEY
        context["route_start_points"] = route_start_points
        context["current_stops"] = current_stops
        return context
    
    
class Approve_Routes(UserPassesTestMixin, LoginRequiredMixin, ListView):
    paginate_by = 3     # https://docs.djangoproject.com/en/4.2/topics/pagination/
    template_name = 'runningApp/approve_routes.html'
    model = Route

    def test_func(self):
        return self.request.user.groups.filter(name='Admins').exists()
    
    def get_queryset(self):
        return super().get_queryset().filter(approved=False)
    
@login_required
def approve(request):
    if(request.method != 'POST'):
        return redirect('approve_routes')
    # print(request.POST)
    route_id = request.POST.get('route_id')
    route = Route.objects.get(id=route_id)
    route.approved = True
    route.save()
    return redirect('approve_routes')

@login_required
def delete(request):
    if(request.method != 'POST'):
        return redirect('approve_routes')
    # print(request.POST)
    route_id = request.POST.get('route_id')
    route = Route.objects.get(id=route_id)
    route.delete()
    return redirect('approve_routes')

@login_required
def create(request):
    print(request.POST)
    if(request.method != 'POST'):
        return redirect('create_route')
    stops_list = json.loads(request.POST.get('stops_list'))
    print(stops_list)


    # Convert gradient_difference to a float
    try:
        gradient_difference = float(request.POST.get('gradient_difference', 0))  # provide a default value if not found
    except ValueError:
        # Handle the error if gradient difference is not a valid float
        # You might want to return an error message or similar
        return JsonResponse({'error': 'Invalid gradient difference value'}, status=400)
    

    # Parse distance and convert to float
    try:
        distance = float(request.POST.get('distance', 0))  # default to 0 if not found
    except ValueError:
        # Handle invalid float conversion
        return JsonResponse({'error': 'Invalid distance value'}, status=400)

    user_id = request.user
    route_name = request.POST.get('title')
    route_desc = request.POST.get('description')
    r = Route(user_id=user_id, route_name=route_name, route_description=route_desc, distance=distance, gradient_range=gradient_difference)
    r.save()

    i = 0
    for stop in stops_list:
        # print(stop["lat"])
        s = Stop(latitude=stop["lat"], longitude=stop["lng"])
        s.save()

        rs = RouteStop(route_id=r, stop_id=s, stop_order=i)
        rs.save()
        print(s.latitude)
        i += 1
    
    print(r)
    return redirect('create_route')