from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('logged-in/', views.logged_in_view, name='logged_in_view'),
    #path('accounts/', include('allauth.urls')),
    # path('map/', views.map_view, name='map'),
    path('weather/', views.weather_view, name='weather'),
    path('logout/', views.logout_view, name='logout'), # make this view
    path('routes/', views.Route_View.as_view(), name='routes'),
]