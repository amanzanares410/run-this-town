from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def index(request):
    return render(request=request, template_name="runningApp/index.html")

@login_required
def logged_in_view(request):
    return render(request, 'logged_in.html')

def logout_view(request):
    logout(request)
    return redirect("/")
