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
    path('logged-in/<int:pk>/', views.Route_Detail.as_view(), name='route_detail'),
    path('approve-routes/', views.Approve_Routes.as_view(), name='approve_routes'),
    path('approve/', views.approve, name='approve'),
    path('create-route/', views.create_route, name='create_route'),
    path('create/', views.create, name='create'),
    path('social/', views.social, name='social'),
    path('delete/', views.delete, name='delete'),
    path('route/<int:pk>/', views.Route_Detail.as_view(), name='route_detail')
]