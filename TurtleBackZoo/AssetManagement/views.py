from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .database_connector import execute_query

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
    query = "SELECT * FROM building;"  # Define your SQL query here
    results, success = execute_query(query, query_type="SELECT")

    if success:
        columns = ['ID', 'name', 'purpose', 'floors']  # Define column names for reference
        
        # Restructuring the data for easier access in the template
        buildings = []
        for row in results:
            building = dict(zip(columns, row))  # Creating a dictionary for each row
            buildings.append(building)
        
        return render(request, 'asset_management/building_actions.html', {'buildings': buildings})
    else:
        return render(request, 'error.html')  # Render an error page or handle failure accordingly

def add_building(request):
    if request.method == 'GET':
        return render(request, 'asset_management/add_building.html')
    elif request.method == 'POST':
        building_name = request.POST.get('building_name')
        purpose = request.POST.get('purpose')
        floors = request.POST.get('floors')

        # Check if building name already exists
        query_check = "SELECT building_id FROM building WHERE building_name = %s"
        result, success = execute_query(query_check, building_name, query_type="SELECT")

        if result:  # If a result is returned, building name already exists
            messages.error(request, 'Building with that name already exists!')
            return render(request, 'asset_management/add_building.html')

        # If building name doesn't exist, proceed with insertion
        query_insert = "INSERT INTO building (building_name, purpose, floors) VALUES (%s, %s, %s)"
        success = execute_query(query_insert, building_name, purpose, floors, query_type="INSERT")

        if success:
            messages.success(request, 'Building added successfully!')
            return redirect('add_building')
        else:
            messages.error(request, 'Failed to add building!')
            return render(request, 'asset_management/add_building.html')

def edit_building(request, building_name):
    # Logic for building actions
    return render(request, 'asset_management/edit_building.html',{'building_name':building_name})


def employee_actions(request):
    # Logic for employee actions
    return render(request, 'asset_management/employee_actions.html')

def attraction_actions(request):
    # Logic for attraction actions
    return render(request, 'asset_management/attraction_actions.html')

def concession_actions(request):
    # Logic for concession actions
    return render(request, 'asset_management/concession_actions.html')