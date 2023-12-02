from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
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
            return redirect('building_actions')
        else:
            messages.error(request, 'Failed to add building!')
            return render(request, 'asset_management/add_building.html')

def edit_building(request, name):
    if request.method == 'GET':
        query = "SELECT * FROM building WHERE building_name = %s;"  # Define your SQL query here
        results, success = execute_query(query, name, query_type="SELECT")
        print("printing Success",success,results)
        if success:
            columns = ['ID', 'name', 'purpose', 'floors']  # Define column names for reference
            
            # Restructuring the data for easier access in the template
            buildings = []
            for row in results:
                building = dict(zip(columns, row))  # Creating a dictionary for each row
                buildings.append(building)
            
            # return render(request, 'asset_management/edit_building.html', {'buildings': buildings})
        
            return render(request, 'asset_management/edit_building.html',{'building_old_name':name,'buildings': buildings})
        else:
            return render(request, 'error.html')  # Render an error page or handle failure accordingly
    
    elif request.method == 'POST':
        building_name = request.POST.get('building_name')
        purpose = request.POST.get('purpose')
        floors = request.POST.get('floors')
        
        # Update building information
        query_update = "UPDATE building SET building_name = %s, purpose = %s, floors = %s WHERE building_name = %s"
        success = execute_query(query_update, building_name, purpose, floors, name, query_type="UPDATE")
        print("printing Success",success)
        
        if success:
            messages.success(request, 'Building updated successfully!')
            return redirect('building_actions')
        else:
            messages.error(request, 'Failed to update building!')
            return render(request, 'asset_management/edit_building.html', {'building_name': name})
           
        

    
    


def delete_building(request, name):
    if request.method == 'POST':
        # Using execute_query for the DELETE operation
        query = "DELETE FROM building WHERE building_name=%s"
        rows_affected, success = execute_query(query, name, query_type="DELETE")

        if success and rows_affected > 0:
            # Redirect if the deletion was successful and at least one row was affected
            return redirect('building_actions')
        
    # Render the delete confirmation page if not a POST request or if deletion failed
    return render(request, 'asset_management/delete_building.html', {'building_name': name})



# def employee_actions(request):
#     # Logic for employee actions
#     return render(request, 'asset_management/employee_actions.html')

def attraction_actions(request):
    # Logic for attraction actions
    return render(request, 'asset_management/attraction_actions.html')

def concession_actions(request):
    # Logic for concession actions
    return render(request, 'asset_management/concession_actions.html')





def employee_actions(request):
    query = "SELECT * FROM employee;"  # Define your SQL query here
    results, success = execute_query(query, query_type="SELECT")

    if success:
        columns = [
            'employee_id', 'first_name', 'middle_name', 'last_name',
            'street', 'city', 'state', 'country', 'zipcode',
            'start_date', 'email', 'phone', 'password',
            'supervisor_id', 'rate_id', 'employee_type'
        ]  # Define column names for reference
        
        # Restructuring the data for easier access in the template
        employees = []
        for row in results:
            employee = dict(zip(columns, row))  # Creating a dictionary for each row
            employees.append(employee)
        
        return render(request, 'asset_management/employee_actions.html', {'employees': employees})
    else:
        return render(request, 'error.html')  # Render an error page or handle failure accordingly

def add_employee(request):
    if request.method == 'GET':
        return render(request, 'asset_management/add_employee.html')
    elif request.method == 'POST':
        # Retrieve employee data from the form
        # Ensure your HTML form fields match these names
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')
        start_date = request.POST.get('start_date')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        supervisor_id = request.POST.get('supervisor_id')
        rate_id = request.POST.get('rate_id')
        employee_type = request.POST.get('employee_type')

        # Check if the employee email already exists
        query_check = "SELECT employee_id FROM employee WHERE email = %s"
        result, success = execute_query(query_check, email, query_type="SELECT")

        if result:  # If a result is returned, the email already exists
            messages.error(request, 'Employee with that email already exists!')
            return render(request, 'asset_management/add_employee.html')

        # If the email doesn't exist, proceed with insertion
        query_insert = """
            INSERT INTO employee (
                first_name, middle_name, last_name,
                street, city, state, country, zipcode,
                start_date, email, phone, password,
                supervisor_id, rate_id, employee_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success = execute_query(
            query_insert,
            first_name, middle_name, last_name,
            street, city, state, country, zipcode,
            start_date, email, phone, password,
            supervisor_id, rate_id, employee_type,
            query_type="INSERT"
        )

        if success:
            messages.success(request, 'Employee added successfully!')
            return redirect('add_employee')
        else:
            messages.error(request, 'Failed to add employee!')
            return render(request, 'asset_management/add_employee.html')

def edit_employee(request, employee_id):
    # Logic for editing employee
    # You need to implement this based on your requirements
    return render(request, 'asset_management/edit_employee.html', {'employee_id': employee_id})

def employee_details(request, employee_id):
    employee = get_object_or_404(employee, id=employee_id)
    return render(request, 'asset_management/employee_details.html', {'employee': employee})