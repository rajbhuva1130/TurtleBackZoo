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

######################################################
#                    Building
######################################################

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



######################################################
#                    Employee
######################################################

def employee_actions(request):
    query = '''SELECT e.emp_number AS "employee_number", e.first_name AS "first_name", e.middle_name AS "middle_name", e.last_name AS "last_name",
                COALESCE(CONCAT(s.first_name, ' ', s.middle_name, ' ', s.last_name), 'N/A') AS "supervisor_name", et.employee_type AS "employee_type" 
                FROM employee e LEFT JOIN employee s ON e.supervisor_id = s.employee_id 
                LEFT JOIN employee_type et ON e.employee_type_id = et.employee_type_id;'''  # Define your SQL query here
    results, success = execute_query(query, query_type="SELECT")

    if success:
        columns = [
            'employee_number', 'first_name', 'middle_name', 'last_name',
            'supervisor_name', 'employee_type'
        ]  # Define column names for reference
        
        # Restructuring the data for easier access in the template
        employees = []
        for row in results:
            employee = dict(zip(columns, row))  # Creating a dictionary for each row
            employees.append(employee)
            
    
        return render(request, 'asset_management/employee/employee_actions.html', {'employees': employees})
    else:
        return render(request, 'error.html')  # Render an error page or handle failure accordingly    

def info_employee(request):
    emp_number = request.GET.get('emp_number')
    emp_type = request.GET.get('emp_type')

    # Retrieve basic employee information
    query = ''' SELECT e.employee_id, e.first_name, e.middle_name, e.last_name, e.street, e.city, e.state, e.country, e.zipcode, e.start_date, e.email, e.phone, e.password, e.supervisor_id, e.employee_type_id, e.emp_number,
            COALESCE(CONCAT(s.first_name, ' ', s.middle_name, ' ', s.last_name), 'N/A') AS "supervisor_name", et.employee_type AS "employee_type"  FROM employee e 
            LEFT JOIN employee s ON e.supervisor_id = s.employee_id 
            LEFT JOIN employee_type et ON e.employee_type_id = et.employee_type_id WHERE e.emp_number = %s '''

    employee_result, success = execute_query(query, emp_number, query_type="SELECT")

    if success and employee_result:
        columns_employee = [
            'employee_id', 'first_name', 'middle_name', 'last_name',
            'street', 'city', 'state', 'country', 'zipcode',
            'start_date', 'email', 'phone', 'password',
            'supervisor_id', 'employee_type_id', 'emp_number', 'supervisor_name', 'employee_type'
        ]

        employee_data = []
        for row in employee_result:
            employee = dict(zip(columns_employee, row))  # Creating a dictionary for each row
            employee_data.append(employee)

        employees_id = employee_data[0]['employee_id']
        
        print("^&%^&^%&^&^%7:", emp_type)

        # Retrieve additional information based on emp_type
        if emp_type == 'Ticket Sellers':
            ticket_seller_query = "SELECT shift FROM ticket_seller WHERE employee_id = %s"
            ticket_seller_result, _ = execute_query(ticket_seller_query, employees_id, query_type="SELECT")
            columns_ticket_seller = ['shift']

            # Add ticket seller information directly to the employee_data dictionary
            for row in ticket_seller_result:
                seller_data = dict(zip(columns_ticket_seller, row))
                employee_data[0].update(seller_data)  # Update the existing dictionary
                

        elif emp_type == 'Customer Service':
            customer_service_query = """SELECT c.concession_name FROM customer_service cs 
                                        LEFT JOIN concession c ON cs.concession_id = c.concession_id WHERE cs.employee_id = %s"""
            customer_service_result, _ = execute_query(customer_service_query, employees_id, query_type="SELECT")
            columns_customer_service = ['concession_name']
            for row in customer_service_result:
                customer_service_data = dict(zip(columns_customer_service, row))
                employee_data[0].update(customer_service_data)

        elif emp_type == 'Maintenance':
            maintenance_query = "SELECT specialization FROM maintenance WHERE employee_id = %s"
            maintenance_result, _ = execute_query(maintenance_query, employees_id, query_type="SELECT")
            columns_maintenance = ['specialization']
            for row in maintenance_result:
                maintenance_data = dict(zip(columns_maintenance, row))
                employee_data[0].update(maintenance_data)

        elif emp_type == 'Veterinarians':
            veterinarian_query = """ SELECT v.license_number, v.degree,  s.species_name FROM veterinarian v 
            LEFT JOIN species s ON v.species_id = s.species_id WHERE v.employee_id = %s """
            veterinarian_result, _ = execute_query(veterinarian_query, employees_id, query_type="SELECT")
            columns_veterinarian = ['license_number', 'degree', 'species_name']
            for row in veterinarian_result:
                veterinarian_data = dict(zip(columns_veterinarian, row))
                employee_data[0].update(veterinarian_data) 

        elif emp_type == 'Animal Care':
            act_query = """ SELECT  act.experience, s.species_name FROM animal_care_trainer_and_specialist act 
                        LEFT JOIN species s ON act.species_id = s.species_id WHERE act.employee_id = %s """
            act_result, _ = execute_query(act_query, employees_id, query_type="SELECT")
            columns_act = [ 'experience',  'species_name']
            for row in act_result:
                act_data = dict(zip(columns_act, row))
                employee_data[0].update(act_data)
            
        print(employee_data)

        # Pass the combined employee_data to the template
        return render(request, 'asset_management/employee/info_employee.html', {'employee_data': employee_data})

    else:
        return render(request, 'error.html')


    
def add_employee(request):
    if request.method == 'GET':
        # Retrieve supervisor names
        supervisor_query = '''
            SELECT DISTINCT  COALESCE(CONCAT(s.first_name, ' ', s.middle_name, ' ', s.last_name)) AS "supervisor_name" ,s.employee_id
            FROM employee e LEFT JOIN employee s ON e.supervisor_id = s.employee_id;
        '''  # Adjust the query as needed

        supervisor_results, success_supervisor = execute_query(supervisor_query, query_type="SELECT")

        if not success_supervisor:
            messages.error(request, 'Failed to fetch supervisor names!')
            return render(request, 'error.html')

        columns_supervisor = ['supervisor_name','supervisor_id']
        supervisors = [dict(zip(columns_supervisor, row)) for row in supervisor_results]
        
        # Retrieve employee types
        employee_type_query = "SELECT DISTINCT employee_type, employee_type_id FROM employee_type;"  # Adjust the query as needed
        results_employee_type, success_employee_type = execute_query(employee_type_query, query_type="SELECT")

        if not success_employee_type:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_employee_type = ['employee_type','employee_type_id']
        employee_types = [dict(zip(columns_employee_type, row)) for row in results_employee_type]
        

        return render(request, 'asset_management/employee/add_employee.html', {'supervisors': supervisors, 'employee_types': employee_types})
    
   
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
        employee_type_id = request.POST.get('employee_type_id')
        emp_type = request.GET.get('emp_type')
        
        # Check if the employee email already exists
        query_check = "SELECT employee_id FROM employee WHERE email = %s"
        result, success = execute_query(query_check, email, query_type="SELECT")
        
        if result:  # If a result is returned, the email already exists
            messages.error(request, 'Employee with that email already exists!')
            return render(request, 'asset_management/employee/add_employee.html')

        # If the email doesn't exist, proceed with insertion
        query_insert = """
            INSERT INTO employee (
                first_name, middle_name, last_name,
                street, city, state, country, zipcode,
                start_date, email, phone, password,
                supervisor_id, employee_type_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success = execute_query(
            query_insert,
            first_name, middle_name, last_name,
            street, city, state, country, zipcode,
            start_date, email, phone, password,
            supervisor_id, employee_type_id,
            query_type="INSERT"
        )

        if success:
            # <!-- Ticket Sellers Section -->
            if employee_type_id == '984b7fb8-dd36-4c96-939d-8bb57583b27c':
                shift = request.POST.get('shift')
                query_insert_ticket_seller ='''INSERT INTO ticket_seller (employee_id, shift) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s)'''
                execute_query(query_insert_ticket_seller,email, shift, query_type="INSERT")

            # <!-- Customer Service Section -->
            elif employee_type_id == 'fb91f4e8-9ce0-46e4-8f1c-30d06dfdd7ad':  
                concession_name = request.POST.get('concession_name')
                query_insert_customer_service = '''INSERT INTO customer_service (employee_id, concession_id) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), (SELECT concession_id FROM concession WHERE concession_name = %s))'''
                execute_query(query_insert_customer_service, email, concession_name, query_type="INSERT")    
                
            # <!-- Maintenance Section -->
            elif employee_type_id == '084efa92-595e-4820-90d7-b330745770f1':
                specialization = request.POST.get('specialization')
                query_insert_maintenance = '''INSERT INTO maintenance (employee_id, specialization) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s)'''
                execute_query(query_insert_maintenance, email, specialization, query_type='INSERT')
            
            # !-- Veterinarians Section -->
            elif employee_type_id == '88f6ea93-ed8b-40c2-a727-6bd40044ef15': 
                license_number = request.POST.get('license_number')
                degree = request.POST.get('degree')
                specie_name = request.POST.get('specie_name')
                query_insert_veterinarian = ''' INSERT INTO veterinarian (employee_id, license_number, degree, species_id) 
                 VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s, %s, (SELECT species_id FROM species WHERE species_name = %s)) '''
                execute_query(query_insert_veterinarian, email, license_number, degree, specie_name, query_type="INSERT")
            
            # <!-- Animal Care Section -->
            elif employee_type_id == '01104a75-e543-40c1-a6dc-175e2d2eb8aa':
                experience = request.POST.get('experience')
                species_name = request.POST.get('species_name')
                query_insert_animal_care = '''INSERT INTO animal_care_trainer_and_specialist (employee_id, experience,species_id) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s,(SELECT species_id FROM species WHERE species_name = %s))'''
                execute_query(query_insert_animal_care, email, experience, species_name, query_type="INSERT")
    
        # Add similar blocks for other employee types    \\\\ also return your emp no is - 
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_actions')
        
        if not success:
            messages.error(request, 'Failed to add employee!')
            return render(request, 'asset_management/employee/add_employee.html')

    else:
        messages.error(request, 'Invalid request method!')
        return render(request, 'error.html')
        


def edit_employee(request, emp_number):
    if request.method == 'GET':
        # Fetch the employee details by name to pre-fill the form
        query = "SELECT * FROM employee WHERE first_name = %s;"  # Adjust the query as needed
        results, success = execute_query(query, emp_number, query_type="SELECT")

        if success and results:
            columns = [
                'employee_id', 'first_name', 'middle_name', 'last_name',
                'street', 'city', 'state', 'country', 'zipcode',
                'start_date', 'email', 'phone', 'password',
                'supervisor_id', 'rate_id', 'employee_type'
            ]
            employee = dict(zip(columns, results[0]))  # Assuming the result is a single record
            return render(request, 'asset_management/employee/edit_employee.html', {'employee': employee})
        else:
            messages.error(request, 'Employee not found!')
            return redirect('employee_actions')

    elif request.method == 'POST':
        # Extract data from form submission
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
    

        # Update employee information in the database
        query_update = """
            UPDATE employee SET 
            first_name = %s, 
            middle_name = %s, 
            last_name = %s,
            street = %s, 
            city = %s, 
            state = %s, 
            country = %s, 
            zipcode = %s, 
            email = %s, 
            phone = %s, 
            password = %s,
            WHERE first_name = %s
        """
        success = execute_query(
            query_update, first_name, middle_name, last_name, street, city, state, country, zipcode, email, phone, password,
            emp_number, query_type="UPDATE"
        )

        if success:
            messages.success(request, 'Employee updated successfully!')
        else:
            messages.error(request, 'Failed to update employee!')
        
        return redirect('employee_actions')




def delete_employee(request, emp_number):
    if request.method == 'POST':
        
        query_delete_animal_care = "DELETE FROM animal_care_trainer_and_specialist WHERE employee_id=(SELECT employee_id FROM employee WHERE emp_number=%s)"
        _, success_animal_care = execute_query(query_delete_animal_care, emp_number, query_type="DELETE")
        
        query_delete_customer_service = "DELETE FROM customer_service WHERE employee_id=(SELECT employee_id FROM employee WHERE emp_number=%s)"
        _, success_customer_service = execute_query(query_delete_customer_service, emp_number, query_type="DELETE")

        query_delete_veterinarian = "DELETE FROM veterinarian WHERE employee_id=(SELECT employee_id FROM employee WHERE emp_number=%s)"
        _, success_veterinarian = execute_query(query_delete_veterinarian, emp_number, query_type="DELETE")

        query_delete_ticket_seller = "DELETE FROM ticket_seller WHERE employee_id=(SELECT employee_id FROM employee WHERE emp_number=%s)"
        _, success_ticket_sellere = execute_query(query_delete_ticket_seller, emp_number, query_type="DELETE")

        query_delete_maintenance = "DELETE FROM maintenance WHERE employee_id=(SELECT employee_id FROM employee WHERE emp_number=%s)"
        _, success_maintenance = execute_query(query_delete_maintenance, emp_number, query_type="DELETE")
        
        # Using execute_query for the DELETE operation
        query = "DELETE FROM employee WHERE emp_number=%s"
        rows_affected, success = execute_query(query, emp_number, query_type="DELETE")

        if success and rows_affected > 0:
            # Redirect if the deletion was successful and at least one row was affected
            return redirect('employee_actions')
        
    # Render the delete confirmation page if not a POST request or if deletion failed
    return render(request, 'asset_management/delete_employee.html', {'employee': emp_number})



######################################################
#                    Attraction
######################################################

def attraction_actions(request):
    # Logic for attraction actions
    return render(request, 'asset_management/attraction_actions.html')



######################################################
#                    Concession
######################################################

def concession_actions(request):
    # Logic for concession actions
    return render(request, 'asset_management/concession_actions.html')