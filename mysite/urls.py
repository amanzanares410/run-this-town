from django.contrib import admin
from django.urls import include, path, re_path
from runningApp.views import index

urlpatterns = [
    path("", index , name="index"),
    path("runningApp/", include("runningApp.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls'))
]

