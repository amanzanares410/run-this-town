from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("runningApp/", include("runningApp.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls'))
]

