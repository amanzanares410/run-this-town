from django.contrib import admin

from runningApp.models import Route, RouteStop, Stop

# Register your models here.

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(RouteStop)