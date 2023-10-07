from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()), # make this view
]