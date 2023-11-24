from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def assetmanagement_home(request):
    return render(request,'home.html',{'name':'assetmanagement_home'})