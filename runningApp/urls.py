from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('logged-in/', views.logged_in_view, name='logged_in_view'),
    #path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls', namespace='social')),
    # path('logout', LogoutView.as_view()), # make this view
]