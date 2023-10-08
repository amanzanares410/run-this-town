from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path()
    path('logged-in/', views.logged_in_view, name='logged_in_view'),
    #path('accounts/', include('allauth.urls')),
    path('logout', views.logout_view) # make this view
]