from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

###################################### Navigation URLS 

def asset_management(request):
    return render(request, 'asset_management/asset_home.html')

def daily_zoo_activity(request):
    return render(request, 'daily_zoo_activity/daily_home.html')

def management_and_reporting(request):
    return render(request, 'management_and_reporting/reports_home.html')

######################################################


def asset_management_home(request):
    return render(request, 'asset_management/asset_home.html',{'name':'assetmanagement_home'})

def building_actions(request):
    # Logic for building actions
    return render(request, 'asset_management/building_actions.html')

def employee_actions(request):
    # Logic for employee actions
    return render(request, 'asset_management/employee_actions.html')

def attraction_actions(request):
    # Logic for attraction actions
    return render(request, 'asset_management/attraction_actions.html')

def concession_actions(request):
    # Logic for concession actions
    return render(request, 'asset_management/concession_actions.html')