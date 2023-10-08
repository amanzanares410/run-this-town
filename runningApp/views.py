from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request=request, template_name="runningApp/index.html")

@login_required
def logged_in_view(request):
    return render(request, 'logged_in.html')