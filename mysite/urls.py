from django.contrib import admin
from django.urls import include, path, re_path
from runningApp.views import logged_in_view 

urlpatterns = [
    path("", logged_in_view , name="logged_in_view"),
    path("runningApp/", include("runningApp.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls'))
]

