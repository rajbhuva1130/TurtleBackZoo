from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def managementandreporting_home(request):
    return render(request,'home.html',{'name':'managementandreporting_home'})