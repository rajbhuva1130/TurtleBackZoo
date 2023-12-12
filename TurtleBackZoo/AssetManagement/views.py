from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .database_connector import execute_query
import bcrypt

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
        
        return render(request, 'asset_management/building/building_actions.html', {'buildings': buildings})
    else:
        return render(request, 'error.html')  # Render an error page or handle failure accordingly

def add_building(request):
    if request.method == 'GET':
        return render(request, 'asset_management/building/add_building.html')
    elif request.method == 'POST':
        building_name = request.POST.get('building_name')
        purpose = request.POST.get('purpose')
        floors = request.POST.get('floors')

        # Check if building name already exists
        query_check = "SELECT building_id FROM building WHERE building_name = %s"
        result, success = execute_query(query_check, building_name, query_type="SELECT")

        if result:  # If a result is returned, building name already exists
            messages.error(request, 'Building with that name already exists!')
            return render(request, 'asset_management/building/add_building.html')

        # If building name doesn't exist, proceed with insertion
        query_insert = "INSERT INTO building (building_name, purpose, floors) VALUES (%s, %s, %s)"
        success = execute_query(query_insert, building_name, purpose, floors, query_type="INSERT")

        if success:
            messages.success(request, 'Building added successfully!')
            return redirect('building_actions')
        else:
            messages.error(request, 'Failed to add building!')
            return render(request, 'asset_management/building/add_building.html')

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
        
            return render(request, 'asset_management/building/edit_building.html',{'building_old_name':name,'buildings': buildings})
        else:
            return render(request, 'error.html')  # Render an error page or handle failure accordingly
    
    elif request.method == 'POST':
        building_name = request.POST.get('building_name')
        purpose = request.POST.get('purpose')
        floors = request.POST.get('floors')
        
        # Update building information
        query_update = "UPDATE building SET building_name = %s, purpose = %s, floors = %s WHERE building_name = %s"
        success = execute_query(query_update, building_name, purpose, floors, name, query_type="UPDATE")

        if success:
            messages.success(request, 'Building updated successfully!')
            return redirect('building_actions')
        else:
            messages.error(request, 'Failed to update building!')
            return render(request, 'asset_management/building/edit_building.html', {'building_name': name})

def delete_building(request, name):
    if request.method == 'POST':
        # Using execute_query for the DELETE operation
        query = "DELETE FROM building WHERE building_name=%s"
        rows_affected, success = execute_query(query, name, query_type="DELETE")

        if success and rows_affected > 0:
            # Redirect if the deletion was successful and at least one row was affected
            return redirect('building_actions')
        

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
        
        # Retrieve concession types
        concession_query = '''SELECT DISTINCT concession_name, concession_id FROM concession;''' 
        result_concession_name, success_concession_name = execute_query(concession_query,query_type="SELECT")
        
        if not success_concession_name:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_concession_name = ['concession_name','concession_id']
        concessions = [dict(zip(columns_concession_name, row)) for row in result_concession_name]
        
        # Retrieve Maintenance Specialization
        maintenance_query = '''SELECT DISTINCT specialization FROM maintenance;''' 
        result_maintenance, success_maintenance = execute_query(maintenance_query,query_type="SELECT")
        
        if not success_maintenance:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_maintenance = ['specialization']
        specializations = [dict(zip(columns_maintenance, row)) for row in result_maintenance]
        
        # Retrieve Spices Name
        species_query = '''SELECT DISTINCT species_name, species_id FROM species;''' 
        result_species, success_species = execute_query(species_query,query_type="SELECT")
        
        if not success_species:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_species = ['species_name','species_id']
        species = [dict(zip(columns_species, row)) for row in result_species]

        return render(request, 'asset_management/employee/add_employee.html', {'supervisors': supervisors, 'employee_types': employee_types, 'concessions':concessions,
                                                                               'specializations':specializations, 'species':species })
    
   
    elif request.method == 'POST':
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
        employee_type = request.POST.get('employee_type')
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        
        # Insert into employee table
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
            start_date, email, phone, hashed_password,
            supervisor_id, employee_type_id,
            query_type="INSERT"
        )

        if success:
            # <!-- Ticket Sellers Section -->
            if employee_type == 'Ticket Sellers':
                shift = request.POST.get('shift')
                query_insert_ticket_seller ='''INSERT INTO ticket_seller (employee_id, shift) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s)'''
                success_ = execute_query(query_insert_ticket_seller,email, shift, query_type="INSERT")
                
                if not success_:
                    query_select_emp_number = "SELECT emp_number FROM employee WHERE email = %s"
                    emp_number = execute_query(query_select_emp_number, email, query_type="SELECT")

                    # Check if emp_number was successfully retrieved
                    if emp_number:
                        delete_employee(emp_number[0])  # Assuming emp_number is returned as a list or tuple
                        messages.error(request, 'Error adding ticket seller details!')
                    else:
                        messages.error(request, 'Failed to retrieve employee details for deletion.')

                    return render(request, 'asset_management/employee/add_employee.html')
                    

            # <!-- Customer Service Section -->
            elif employee_type == 'Customer Service':  
                concession_name = request.POST.get('concession_name')
                query_insert_customer_service = '''INSERT INTO customer_service (employee_id, concession_id) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), (SELECT concession_id FROM concession WHERE concession_name = %s))'''
                success_ = execute_query(query_insert_customer_service, email, concession_name, query_type="INSERT")
                
                if not success_:
                    query_select_emp_number = "SELECT emp_number FROM employee WHERE email = %s"
                    emp_number = execute_query(query_select_emp_number, email, query_type="SELECT")

                    # Check if emp_number was successfully retrieved
                    if emp_number:
                        delete_employee(emp_number[0])  # Assuming emp_number is returned as a list or tuple
                        messages.error(request, 'Error adding ticket seller details!')
                    else:
                        messages.error(request, 'Failed to retrieve employee details for deletion.')

                    return render(request, 'asset_management/employee/add_employee.html')    
                
            # <!-- Maintenance Section -->
            elif employee_type == 'Maintenance':
                specialization = request.POST.get('specialization')
                query_insert_maintenance = '''INSERT INTO maintenance (employee_id, specialization) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s)'''
                success_ = execute_query(query_insert_maintenance, email, specialization, query_type='INSERT')
                
                if not success_:
                    query_select_emp_number = "SELECT emp_number FROM employee WHERE email = %s"
                    emp_number = execute_query(query_select_emp_number, email, query_type="SELECT")

                    # Check if emp_number was successfully retrieved
                    if emp_number:
                        delete_employee(emp_number[0])  # Assuming emp_number is returned as a list or tuple
                        messages.error(request, 'Error adding ticket seller details!')
                    else:
                        messages.error(request, 'Failed to retrieve employee details for deletion.')

                    return render(request, 'asset_management/employee/add_employee.html') 
            
            # !-- Veterinarians Section -->
            elif employee_type == 'Veterinarians': 
                license_number = request.POST.get('license_number')
                degree = request.POST.get('degree')
                specie_id = request.POST.get('specie_id')
                query_insert_veterinarian = ''' INSERT INTO veterinarian (employee_id, license_number, degree, species_id) 
                 VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s, %s, %s) '''
                success_ = execute_query(query_insert_veterinarian, email, license_number, degree, specie_id, query_type="INSERT")
                
                if not success_:
                    query_select_emp_number = "SELECT emp_number FROM employee WHERE email = %s"
                    emp_number = execute_query(query_select_emp_number, email, query_type="SELECT")

                    # Check if emp_number was successfully retrieved
                    if emp_number:
                        delete_employee(emp_number[0])  # Assuming emp_number is returned as a list or tuple
                        messages.error(request, 'Error adding ticket seller details!')
                    else:
                        messages.error(request, 'Failed to retrieve employee details for deletion.')

                    return render(request, 'asset_management/employee/add_employee.html') 
            
            # <!-- Animal Care Section -->
            elif employee_type == 'Animal Care':
                experience = request.POST.get('experience')
                species_id = request.POST.get('species_id')
                query_insert_animal_care = '''INSERT INTO animal_care_trainer_and_specialist (employee_id, experience,species_id) 
                VALUES ((SELECT employee_id FROM employee WHERE email = %s), %s, %s)'''
                success_ = execute_query(query_insert_animal_care, email, experience, species_id, query_type="INSERT")
                
                if not success_:
                    query_select_emp_number = "SELECT emp_number FROM employee WHERE email = %s"
                    emp_number = execute_query(query_select_emp_number, email, query_type="SELECT")

                    # Check if emp_number was successfully retrieved
                    if emp_number:
                        delete_employee(emp_number[0])  # Assuming emp_number is returned as a list or tuple
                        messages.error(request, 'Error adding ticket seller details!')
                    else:
                        messages.error(request, 'Failed to retrieve employee details for deletion.')

                    return render(request, 'asset_management/employee/add_employee.html') 
    
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
        emp_type = request.GET.get('emp_type')
        # Retrieve employee types
        employee_type_query = "SELECT DISTINCT employee_type, employee_type_id FROM employee_type;"  # Adjust the query as needed
        results_employee_type, success_employee_type = execute_query(employee_type_query, query_type="SELECT")

        if not success_employee_type:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_employee_type = ['employee_type','employee_type_id']
        employee_types = [dict(zip(columns_employee_type, row)) for row in results_employee_type]
        
        # Retrieve concession types
        concession_query = '''SELECT DISTINCT concession_name, concession_id FROM concession;''' 
        result_concession_name, success_concession_name = execute_query(concession_query,query_type="SELECT")
        
        if not success_concession_name:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_concession_name = ['concession_name','concession_id']
        concessions = [dict(zip(columns_concession_name, row)) for row in result_concession_name]
        
        # Retrieve Maintenance Specialization
        maintenance_query = '''SELECT DISTINCT specialization FROM maintenance;''' 
        result_maintenance, success_maintenance = execute_query(maintenance_query,query_type="SELECT")
        
        if not success_maintenance:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_maintenance = ['specialization']
        specializations = [dict(zip(columns_maintenance, row)) for row in result_maintenance]
        
        # Retrieve Spices Name
        species_query = '''SELECT DISTINCT species_name, species_id FROM species;''' 
        result_species, success_species = execute_query(species_query,query_type="SELECT")
        
        if not success_species:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_species = ['species_name','species_id']
        species = [dict(zip(columns_species, row)) for row in result_species]
        
        employee_data = []
        # Fetch the employee details by name to pre-fill the form
        query = "SELECT * FROM employee WHERE emp_number = %s;"  # Adjust the query as needed
        results, success = execute_query(query, emp_number, query_type="SELECT")

        if success and results:
            columns = [
                'employee_id', 'first_name', 'middle_name', 'last_name',
                'street', 'city', 'state', 'country', 'zipcode',
                'start_date', 'email', 'phone', 'password',
                'supervisor_id', 'employee_type_id','emp_number'
            ]
            employee = dict(zip(columns, results[0]))
            employee_data.append(employee)
            
        # ticket seller
        ticket_query = '''SELECT shift FROM ticket_seller WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);''' 
        result_ticket, success_ticket = execute_query(ticket_query,emp_number,query_type="SELECT")
        if not success_ticket:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')
        columns_ticket = ['shift']
        for row in result_ticket:
            ticket_sellers = dict(zip(columns_ticket, row)) 
            employee_data[0].update(ticket_sellers)

        
        # customer service
        customer_query = '''SELECT concession_id FROM customer_service WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);''' 
        result_customer, success_customer = execute_query(customer_query,emp_number,query_type="SELECT")
        if not success_customer:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')
        columns_customer = ['concession_id']
        for row in result_customer:
            customer = dict(zip(columns_customer, row)) 
            employee_data[0].update(customer)
        
        # Maintenance
        maintenance_query = "SELECT specialization FROM maintenance WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);"
        maintenance_result, success_Maintenance = execute_query(maintenance_query, emp_number, query_type="SELECT")
        if not success_Maintenance:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')
        columns_maintenance = ['specialization']
        for row in maintenance_result:
            maintenance_data = dict(zip(columns_maintenance, row))
            employee_data[0].update(maintenance_data)
        
        #Veterinarians
        veterinarian_query = """ SELECT v.license_number, v.degree, v.species_id, s.species_name FROM veterinarian v 
        LEFT JOIN species s ON v.species_id = s.species_id WHERE v.employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s); """
        veterinarian_result, success_Veterinarians = execute_query(veterinarian_query, emp_number, query_type="SELECT")
        if not success_Veterinarians:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')
        columns_veterinarian = ['license_number', 'degree','specie_id', 'species_name']
        for row in veterinarian_result:
            veterinarian_data = dict(zip(columns_veterinarian, row))
            employee_data[0].update(veterinarian_data) 

        #Animal Care
        act_query = """ SELECT  act.experience,act.species_id, s.species_name FROM animal_care_trainer_and_specialist act 
                    LEFT JOIN species s ON act.species_id = s.species_id WHERE act.employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s); """
        act_result, success_act = execute_query(act_query, emp_number, query_type="SELECT")
        if not success_act:
                messages.error(request, 'Failed to fetch employee types!')
                return render(request, 'error.html')
        columns_act = [ 'experience', 'species_id', 'species_name']
        for row in act_result:
            act_data = dict(zip(columns_act, row))
            employee_data[0].update(act_data)
        
        return render(request, 'asset_management/employee/edit_employee.html', {'employee_types':employee_types,'concessions':concessions,
                                                                               'specializations':specializations, 'species':species,'employee_data':employee_data})

    elif request.method == 'POST':
        # Extract data from form submission
        current_type_id = request.POST.get('current_type_id') 
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
        employee_type_id = request.POST.get('employee_type_id')
        employee_type = request.POST.get('employee_type')
        
        # Get the existing employee type for the employee
        query_get_current_type = "SELECT employee_type FROM employee_type WHERE employee_type_id = %s;"
        current_type_, success_current_type = execute_query(query_get_current_type, current_type_id, query_type="SELECT")
        current_type = current_type_[0][0]
        
        # Check if the current employee type is retrieved successfully
        if not success_current_type or not current_type:
            messages.error(request, 'Failed to fetch current employee type!')
            return redirect('employee_actions')
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)

        # Update employee information in the database
        query_update = """ UPDATE employee SET first_name = %s, middle_name = %s, last_name = %s, street = %s, 
        city = %s, state = %s, country = %s, zipcode = %s, email = %s, phone = %s, password = %s,
        employee_type_id = %s WHERE emp_number = %s"""
        success = execute_query(
            query_update, first_name, middle_name, last_name, street, city, state, country, zipcode, email, phone, hashed_password, employee_type_id,
            emp_number, query_type="UPDATE"
        )
        
        if not success:
            messages.error(request, 'Failed to update employee information!')
            return render(request, 'asset_management/employee/edit_employee.html') 

        else:
            
            def delete_previous_employee_type_data(current_type, emp_number):
                type_table_map = {
                    'Ticket Sellers': ('ticket_seller', 'employee_id'),
                    'Customer Service': ('customer_service', 'employee_id'),
                    'Maintenance': ('maintenance', 'employee_id'),
                    'Veterinarians': ('veterinarian', 'employee_id'),
                    'Animal Care': ('animal_care_trainer_and_specialist', 'employee_id')
                }

                result = type_table_map.get(current_type)
                if result:
                    table, employee_id = result
                    query_delete = f"DELETE FROM {table} WHERE {employee_id} = (SELECT employee_id FROM employee WHERE emp_number = %s);"
                    try:
                        execute_query(query_delete, emp_number, query_type="DELETE")
                    except Exception as e:
                        print(f"Error while executing delete query: {e}")
                else:
                    print(f"No mapping found for emp_type_id: {current_type_id}")


            # Check if the employee type has changed
            if current_type != employee_type:
                # Delete data from the previous employee type table
                delete_previous_employee_type_data(current_type,emp_number)
            
                # <!-- Ticket Sellers Section -->
                if employee_type == 'Ticket Sellers':
                    shift = request.POST.get('shift')
                    query_insert_ticket_seller ='''INSERT INTO ticket_seller (employee_id, shift) 
                    VALUES ((SELECT employee_id FROM employee WHERE emp_number = %s), %s)'''
                    success_ = execute_query(query_insert_ticket_seller,emp_number, shift, query_type="INSERT")
                    
                # <!-- Customer Service Section -->
                elif employee_type == 'Customer Service':  
                    concession_id = request.POST.get('concession_id')
                    query_insert_customer_service = '''INSERT INTO customer_service (employee_id, concession_id) 
                    VALUES ((SELECT employee_id FROM employee WHERE emp_number = %s), %s)'''
                    success_ = execute_query(query_insert_customer_service, emp_number, concession_id, query_type="INSERT")
                    
                # <!-- Maintenance Section -->
                elif employee_type == 'Maintenance':
                    specialization = request.POST.get('specialization')
                    query_insert_maintenance = '''INSERT INTO maintenance (employee_id, specialization) 
                    VALUES ((SELECT employee_id FROM employee WHERE emp_number = %s), %s)'''
                    success_ = execute_query(query_insert_maintenance, emp_number, specialization, query_type='INSERT')
                
                # !-- Veterinarians Section -->
                elif employee_type == 'Veterinarians': 
                    license_number = request.POST.get('license_number')
                    degree = request.POST.get('degree')
                    specie_id = request.POST.get('specie_id')
                    query_insert_veterinarian = ''' INSERT INTO veterinarian (employee_id, license_number, degree, species_id) 
                    VALUES ((SELECT employee_id FROM employee WHERE emp_number = %s), %s, %s, %s) '''
                    success_ = execute_query(query_insert_veterinarian, emp_number, license_number, degree, specie_id, query_type="INSERT")
                
                # <!-- Animal Care Section -->
                elif employee_type == 'Animal Care':
                    experience = request.POST.get('experience')
                    species_id = request.POST.get('species_id')
                    query_insert_animal_care = '''INSERT INTO animal_care_trainer_and_specialist (employee_id, experience,species_id) 
                    VALUES ((SELECT employee_id FROM employee WHERE emp_number = %s), %s, %s)'''
                    success_ = execute_query(query_insert_animal_care, emp_number, experience, species_id, query_type="INSERT")
            
            else:
                # <!-- Ticket Sellers Section -->
                if employee_type == 'Ticket Sellers':
                    shift = request.POST.get('shift')
                    query_insert_ticket_seller ='''UPDATE ticket_seller SET shift = %s 
                    WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);'''
                    success_ = execute_query(query_insert_ticket_seller,shift, emp_number,  query_type="UPDATE")
                    
                # <!-- Customer Service Section -->
                elif employee_type == 'Customer Service':  
                    concession_id = request.POST.get('concession_id')
                    query_insert_customer_service = '''UPDATE customer_service SET concession_id = %s 
                    WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);'''
                    success_ = execute_query(query_insert_customer_service, concession_id, emp_number, query_type="UPDATE")
                    
                # <!-- Maintenance Section -->
                elif employee_type == 'Maintenance':
                    specialization = request.POST.get('specialization')
                    query_insert_maintenance = '''UPDATE maintenance SET specialization = %s 
                    WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);'''
                    success_ = execute_query(query_insert_maintenance,specialization, emp_number,  query_type='UPDATE')
                
                # !-- Veterinarians Section -->
                elif employee_type == 'Veterinarians': 
                    license_number = request.POST.get('license_number')
                    degree = request.POST.get('degree')
                    specie_id = request.POST.get('specie_id')
                    query_insert_veterinarian = '''UPDATE veterinarian SET license_number = %s, degree = %s, species_id = %s
                    WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);'''
                    success_ = execute_query(query_insert_veterinarian, license_number, degree, specie_id,emp_number, query_type="UPDATE")
                
                # <!-- Animal Care Section -->
                elif employee_type == 'Animal Care':
                    experience = request.POST.get('experience')
                    species_id = request.POST.get('species_id')
                    query_insert_animal_care = '''UPDATE animal_care_trainer_and_specialist SET experience = %s, species_id = %s 
                    WHERE employee_id = (SELECT employee_id FROM employee WHERE emp_number = %s);'''
                    success_ = execute_query(query_insert_animal_care,  experience, species_id, emp_number, query_type="UPDATE")      

            messages.success(request, 'Employee Updated successfully!')
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
    query = '''SELECT a.attraction_id, a.attraction_name, a.seats, b.building_name
    FROM attraction a INNER JOIN building b ON a.building_id = b.building_id;''' 

    attractions_results, attractions_success = execute_query(query, query_type="SELECT")
    
    if not attractions_success:
        messages.error(request, "Failed to load attractions.")
        return render(request, 'error.html')

    attractions_columns = ['attraction_id', 'attraction_name', 'seats', 'building_name']  
    attractions = [dict(zip(attractions_columns, row)) for row in attractions_results]
    
    # Query to fetch requirements for each attraction
    requirements_query = '''SELECT ar.attraction_id, s.species_name, ar.quantity
    FROM attraction_requirement ar INNER JOIN species s ON ar.species_id = s.species_id;'''
    
    # Execute the query
    requirements_results, requirements_success = execute_query(requirements_query, query_type="SELECT")

    if not requirements_success:
        messages.error(request, "Failed to load attraction requirements.")
        return render(request, 'error.html')

    # Process attractions results
    attractions = [dict(zip(['attraction_id', 'attraction_name', 'seats', 'building_name'], attraction)) for attraction in attractions_results]

    # Create a dictionary to map attraction IDs to their requirements
    requirements_mapping = {}
    for req in requirements_results:
        attraction_id, species_name, quantity = req
        if attraction_id in requirements_mapping:
            requirements_mapping[attraction_id].append({'species_name': species_name, 'quantity': quantity})
        else:
            requirements_mapping[attraction_id] = [{'species_name': species_name, 'quantity': quantity}]

    # Add requirements to each attraction in the list
    for attraction in attractions:
        attraction_id = attraction['attraction_id']
        attraction['requirements'] = requirements_mapping.get(attraction_id, [])
    
    return render(request, 'asset_management/attraction/attraction_actions.html', {'attractions': attractions})
    
def add_attraction(request):
    if request.method == 'GET':
        # Fetch buildings from the database
        query = "SELECT building_id, building_name FROM building;"
        buildings, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_buildings = ['building_id','building_name']
        buildings = [dict(zip(columns_buildings, row)) for row in buildings]
        
        # Fetch species from the database
        species_query = "SELECT species_id, species_name FROM species;"
        species, species_success = execute_query(species_query, query_type="SELECT")

        if not species_success:
            messages.error(request, 'Failed to fetch species!')
            return render(request, 'error.html')

        columns_species = ['species_id', 'species_name']
        species = [dict(zip(columns_species, row)) for row in species]
        
        
        return render(request, 'asset_management/attraction/add_attraction.html', {'buildings': buildings, 'species': species})
        
    if request.method == 'POST':
        attraction_name = request.POST.get('attraction_name')
        seats = request.POST.get('seats')
        building_id = request.POST.get('building_id')

        # Inserting a new attraction
        query_insert = "INSERT INTO attraction (attraction_name, seats, building_id) VALUES (%s, %s, %s);"
        results, success = execute_query(query_insert, attraction_name, seats, building_id,query_type="INSERT")
        
        if not success:
            messages.error(request, 'Failed to add attraction!')
            return render(request, 'asset_management/attraction/add_attraction.html')
        
        query_att_id = "SELECT attraction_id FROM attraction WHERE attraction_name = %s;"
        attraction_id_results, _ = execute_query(query_att_id,attraction_name,query_type="SELECT")

        if not success:
            messages.error(request, 'Failed to add attraction!')
            return render(request, 'asset_management/attraction/add_attraction.html')

        attraction_id = attraction_id_results[0][0]

        # Retrieve and process multiple species and quantities
        species_ids = request.POST.getlist('species_id[]')
        quantities = request.POST.getlist('quantity[]')

        for species_id, quantity in zip(species_ids, quantities):
            requirement_insert_query = "INSERT INTO attraction_requirement (attraction_id, species_id, quantity) VALUES (%s, %s, %s);"
            execute_query(requirement_insert_query, attraction_id, species_id, quantity,query_type="INSERT")

        messages.success(request, 'Attraction added successfully!')
        return redirect('attraction_actions')

    return render(request, 'asset_management/attraction/add_attraction.html')

def edit_attraction(request, attraction_name):
    if request.method == 'GET':
        # Fetch the attraction details along with the building name
        query = '''SELECT a.attraction_id, a.attraction_name, a.seats, b.building_name, a.building_id
        FROM attraction a
        INNER JOIN building b ON a.building_id = b.building_id
        WHERE a.attraction_name = %s;'''
        results, success = execute_query(query, attraction_name, query_type="SELECT")

        if success:
            columns = ['attraction_id', 'attraction_name', 'seats', 'building_name','building_id']
            attractions = [dict(zip(columns, row)) for row in results]

            # Also fetch all buildings for the dropdown list in the edit form
            query = "SELECT building_id, building_name FROM building;"
            buildings, success = execute_query(query, query_type="SELECT")
            
            if not success:
                messages.error(request, 'Failed to fetch employee types!')
                return render(request, 'error.html')

            columns_buildings = ['building_id','building_name']
            buildings = [dict(zip(columns_buildings, row)) for row in buildings]
            
            # Fetch species from the database
            species_query = "SELECT species_id, species_name FROM species;"
            species, species_success = execute_query(species_query, query_type="SELECT")

            if not species_success:
                messages.error(request, 'Failed to fetch species!')
                return render(request, 'error.html')

            columns_species = ['species_id', 'species_name']
            species = [dict(zip(columns_species, row)) for row in species]
            
        # Fetch the current requirements for the attraction
            requirement_query = '''SELECT species_id, quantity FROM attraction_requirement 
            WHERE attraction_id = (SELECT attraction_id FROM attraction WHERE attraction_name = %s);'''
            requirement_results, requirement_success = execute_query(requirement_query, attraction_name, query_type="SELECT")

            if not requirement_success:
                messages.error(request, 'Failed to fetch attraction requirements!')
                return render(request, 'error.html')    
            columns_requirements = ['species_id', 'quantity']
            requirements = [dict(zip(columns_requirements, row)) for row in requirement_results]

            return render(request, 'asset_management/attraction/edit_attraction.html', {'attractions': attractions, 'buildings': buildings, 'requirements': requirements,'species': species})

        else:
            messages.error(request, "Failed to load attraction data.")
            return render(request, 'error.html')  # Render an error page or handle failure accordingly

    elif request.method == 'POST':
        current_attraction_name = request.POST.get('current_attraction_name')  # This is the original name before update
        new_attraction_name = request.POST.get('attraction_name')  # This is the new name you want to update to
        seats = request.POST.get('seats')
        building_id = request.POST.get('building_id')
        
        get_attraction_id_query = "SELECT attraction_id FROM attraction WHERE attraction_name = %s;"
        attraction_id_results, attraction_id_success = execute_query(get_attraction_id_query, current_attraction_name, query_type="SELECT")
        if not attraction_id_success:
            messages.error(request, 'Failed to find attraction!')
            return render(request, 'asset_management/attraction/add_attraction.html')
        attraction_id = attraction_id_results[0][0]

        # Update attraction information
        query_update = "UPDATE attraction SET attraction_name = %s, seats = %s, building_id = %s WHERE attraction_name = %s"
        success = execute_query(query_update, new_attraction_name, seats, building_id, current_attraction_name, query_type="UPDATE")
        
        # Retrieve additional fields for requirements
        current_species_id = request.POST.get('current_species_id')
        species_id = request.POST.get('species_id')
        quantity = request.POST.get('quantity')
 
        # Update the requirement information
        if (current_species_id != species_id):
            delete_query = "DELETE FROM attraction_requirement WHERE attraction_id = %s AND species_id = %s;"
            delete_success = execute_query(delete_query, attraction_id, current_species_id, query_type="DELETE")

            if not delete_success:
                messages.error(request, 'Failed to update attraction requirement!')
                return render(request, 'asset_management/attraction/edit_attraction.html')
            
            if delete_success:
                insert_query = "INSERT INTO attraction_requirement (attraction_id, species_id, quantity) VALUES (%s, %s, %s);"
                insert_success = execute_query(insert_query, attraction_id, species_id, quantity, query_type="INSERT")

                if not insert_success:
                    messages.error(request, 'Failed to update attraction requirement!')
                    return render(request, 'asset_management/attraction/edit_attraction.html')
        
            return redirect('attraction_actions')
            
 
        else:
            requirement_update_query = '''UPDATE attraction_requirement SET quantity = %s WHERE attraction_id = %s AND species_id = %s;'''
            requirement_success = execute_query (requirement_update_query, quantity, attraction_id, species_id, query_type="UPDATE")

            if not requirement_success:
                messages.error(request, 'Failed to update attraction requirements!')
                return render(request, 'asset_management/attraction/edit_attraction.html', {'attraction_name': current_attraction_name})

            if success:
                messages.success(request, 'Attraction updated successfully!')
                return redirect('attraction_actions')
            else:
                messages.error(request, 'Failed to update attraction!')
                # Render the edit page again with the current attraction information
                return render(request, 'asset_management/attraction/edit_attraction.html', {'attraction_name': current_attraction_name})

def delete_attraction(request, attraction_name):
    if request.method == 'POST':
        # First, delete the related requirements in attraction_requirement
        delete_requirements_query = "DELETE FROM attraction_requirement WHERE attraction_id IN (SELECT attraction_id FROM attraction WHERE attraction_name = %s)"
        _, req_delete_success = execute_query(delete_requirements_query, attraction_name, query_type="DELETE")

        if not req_delete_success:
            messages.error(request, 'Failed to delete attraction requirements!')
            return redirect('attraction_actions')

        # Deleting an attraction
        query = "DELETE FROM attraction WHERE attraction_name = %s"
        rows_affected, success = execute_query(query, attraction_name, query_type="DELETE")

        if success and rows_affected > 0:
            messages.success(request, 'Attraction deleted successfully!')
            return redirect('attraction_actions')
        else:
            messages.error(request, 'Failed to delete attraction!')

######################################################
#                    Concession
######################################################

def concession_actions(request):
    # Assuming 'execute_query' is a utility function you've defined to run database queries
    query = "SELECT concession_id, concession_name FROM concession;"
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load concessions.")
        return render(request, 'error.html') 
    
    columns_concession = ['concession_id','concession_name']
    concessions = [dict(zip(columns_concession, row)) for row in results]

    return render(request, 'asset_management/concession/concession_actions.html', {'concessions': concessions}) 
    
def add_concession(request):
    if request.method == 'POST':
        concession_name = request.POST.get('concession_name')
        query = "INSERT INTO concession (concession_name) VALUES (%s);"
        success = execute_query(query, concession_name, query_type="INSERT")

        if success:
            messages.success(request, "New concession added successfully.")
            return redirect('concession_actions')
        else:
            messages.error(request, "There was an error adding the concession.")

    return render(request, 'asset_management/concession/add_concession.html')

def edit_concession(request, concession_name):
    if request.method == 'GET':
        query = '''SELECT concession_id, concession_name
        FROM concession WHERE concession_name = %s;'''
        results, success = execute_query(query, concession_name, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_concession = ['concession_id','concession_name']
        concessions = [dict(zip(columns_concession, row)) for row in results]

        return render(request, 'asset_management/concession/edit_concession.html', {'concessions': concessions})
    
    
    if request.method == 'POST':
        current_concession_name = request.POST.get('current_concession_name') 
        concession_name = request.POST.get('concession_name')
        # Assume you have a function execute_query that handles your database interaction
        query = "UPDATE concession SET concession_name = %s WHERE concession_name = %s;"
        success = execute_query(query, concession_name, current_concession_name, query_type="UPDATE")

        if success:
            messages.success(request, "Concession updated successfully.")
            return redirect('concession_actions')
        else:
            messages.error(request, "There was an error updating the concession.")

    return render(request, 'asset_management/concession/edit_concession.html', {'concessions': concessions})

def delete_concession(request, concession_name):
    if request.method == 'POST':
        # Perform the delete operation
        query = "DELETE FROM concession WHERE concession_name = %s;"
        success = execute_query(query, concession_name, query_type="DELETE")
        
        if success:
            messages.success(request, "Concession deleted successfully.")
            return redirect('concession_actions')
        else:
            messages.error(request, "There was an error deleting the concession.")
            return redirect('concession_actions')

######################################################
#                    Animal
######################################################
def animal_actions(request):
    query = '''SELECT a.animal_id, s.species_name, s.species_type,s.species_id,e.enclosure_id, e.enclosure_number, a.status, a.birth_year, a.tag_number
    FROM animals a JOIN species s ON a.species_id = s.species_id JOIN enclosure e ON a.enclosure_id = e.enclosure_id;'''
    Results, success = execute_query(query, None, query_type="SELECT")

    if not success:
        messages.error(request, "Failed to load concessions.")
        return render(request, 'error.html') 
    
    columns_Animal = ['animal_id','species_name','species_type','species_id','enclosure_id','enclosure_number','status','birth_year','tag_number' ]
    animals = [dict(zip(columns_Animal, row)) for row in Results]  

    return render(request, 'asset_management/animal/animal_action.html', {'animals': animals}) 
       
def add_animal(request):
    if request.method == 'GET':
        # Fetch species from the database
        species_query = "SELECT species_id, species_name FROM species;"
        species, species_success = execute_query(species_query, query_type="SELECT")

        if not species_success:
            messages.error(request, 'Failed to fetch species!')
            return render(request, 'error.html')

        columns_species = ['species_id', 'species_name']
        species = [dict(zip(columns_species, row)) for row in species]
        
        # Fetch enclosure from the database
        enclosure_query = "SELECT enclosure_number, enclosure_id FROM enclosure;"
        enclosure, enclosure_success = execute_query(enclosure_query, query_type="SELECT")

        if not enclosure_success:
            messages.error(request, 'Failed to fetch enclosures!')
            return render(request, 'error.html')

        columns_enclosure = ['enclosure_number', 'enclosure_id']
        enclosures = [dict(zip(columns_enclosure, row)) for row in enclosure]
        
        return render(request, 'asset_management/animal/add_animal.html',{'species': species,'enclosures': enclosures} )

    elif request.method == 'POST':
        # Retrieve data from form
        species_id = request.POST['species_id']
        enclosure_id = request.POST['enclosure_id']
        status = request.POST['status']
        birth_year = request.POST['birth_year']

        # Insert data into the database
        insert_query = "INSERT INTO animals (species_id, enclosure_id, status, birth_year) VALUES (%s, %s, %s, %s)"
        execute_query(insert_query, species_id, enclosure_id, status, birth_year, query_type="INSERT")
        
        return redirect('animal_actions')  # Redirect to the list of animals
    
def edit_animal(request, tag_number):
    if request.method == 'GET':
        # Fetch the specific animal's details using its ID
        query = '''SELECT a.animal_id,a.species_id, s.species_name, a.enclosure_id, e.enclosure_number, a.status, a.birth_year,a.tag_number
        FROM animals a JOIN species s ON a.species_id = s.species_id JOIN enclosure e ON a.enclosure_id = e.enclosure_id
        WHERE a.tag_number = %s;'''
        Results, success = execute_query(query, tag_number, query_type="SELECT")

        if not success:
            messages.error(request, "Failed to load concessions.")
            return render(request, 'error.html') 
        
        columns_Animal = ['animal_id','species_id','species_name','enclosure_id','enclosure_number','status','birth_year','tag_number' ]
        animals = [dict(zip(columns_Animal, row)) for row in Results]
        
        # Fetch species from the database
        species_query = "SELECT species_id, species_name FROM species;"
        species, species_success = execute_query(species_query, query_type="SELECT")

        if not species_success:
            messages.error(request, 'Failed to fetch species!')
            return render(request, 'error.html')

        columns_species = ['species_id', 'species_name']
        species = [dict(zip(columns_species, row)) for row in species]
        
        # Fetch enclosure from the database
        enclosure_query = "SELECT enclosure_number, enclosure_id FROM enclosure;"
        enclosure, enclosure_success = execute_query(enclosure_query, query_type="SELECT")

        if not enclosure_success:
            messages.error(request, 'Failed to fetch enclosures!')
            return render(request, 'error.html')

        columns_enclosure = ['enclosure_number', 'enclosure_id']
        enclosures = [dict(zip(columns_enclosure, row)) for row in enclosure]

        return render(request, 'asset_management/animal/edit_animal.html', {'animals': animals,'species': species,'enclosures': enclosures})
        

    if request.method == 'POST':
        # Retrieve updated data from form
        species_id = request.POST.get('species_id')
        enclosure_id = request.POST.get('enclosure_id')
        status = request.POST.get('status')
        birth_year = request.POST.get('birth_year')
        
        # Update the animal's data in the database
        update_query = "UPDATE animals SET species_id = %s, enclosure_id = %s, status = %s, birth_year = %s WHERE tag_number = %s"
        success = execute_query(update_query, species_id, enclosure_id, status, birth_year, tag_number, query_type="UPDATE")
        
        if success:
            messages.success(request, 'Animal updated successfully!')
            return redirect('animal_actions')  # Redirect to the list of animals
        else:
            messages.error(request, "There was an error updating the concession.")
    
    return render(request, 'asset_management/animal/edit_animal.html', {'animals': animals,'species': species,'enclosures': enclosures})

def delete_animal(request, tag_number):
    if request.method == 'POST':
        delete_query = "DELETE FROM animals WHERE tag_number = %s"
        execute_query(delete_query, tag_number, query_type="DELETE")

        return redirect('animal_actions')

######################################################
#                    Enclosure
######################################################

def enclosure_actions(request):
    query = '''SELECT e.enclosure_id, e.square_foot, e.enclosure_number,e.building_id, b.building_name
    FROM enclosure e JOIN building b ON e.building_id = b.building_id;'''
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load enclosures.")
        return render(request, 'error.html')
    
    columns_enclosure = ['enclosure_id','square_foot','enclosure_number','building_id','building_name' ]
    enclosures = [dict(zip(columns_enclosure, row)) for row in results] 

    return render(request, 'asset_management/enclosure/enclosure_actions.html', {'enclosures': enclosures})

def add_enclosure(request):
    if request.method == 'GET':
        # Fetch buildings from the database
        query = "SELECT building_id, building_name FROM building;"
        buildings, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_buildings = ['building_id','building_name']
        buildings = [dict(zip(columns_buildings, row)) for row in buildings]
        
        return render(request,'asset_management/enclosure/add_enclosure.html',{'buildings' :buildings})

    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        square_foot = request.POST.get('square_foot')
        enclosure_number = request.POST.get('enclosure_number')

        query = "INSERT INTO enclosure (building_id, square_foot, enclosure_number) VALUES (%s, %s, %s);"
        success = execute_query(query, building_id, square_foot, enclosure_number, query_type="INSERT")

        if success:
            messages.success(request, "New enclosure added successfully.")
            return redirect('enclosure_actions')
        else:
            messages.error(request, "There was an error adding the enclosure.")

    return render(request, 'asset_management/enclosure/add_enclosure.html')

def edit_enclosure(request, enclosure_number):
    if request.method == 'GET':
        query = "SELECT * FROM enclosure WHERE enclosure_number = %s;"
        results, success = execute_query(query, enclosure_number, query_type="SELECT")

        if not success:
            messages.error(request, "Failed to fetch the enclosure.")
            return render(request, 'error.html')
        
        columns_enclosure = ['enclosure_id','building_id','square_foot','enclosure_number' ]
        enclosures = [dict(zip(columns_enclosure, row)) for row in results] 
        
        # Fetch buildings from the database
        query = "SELECT building_id, building_name FROM building;"
        buildings, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_buildings = ['building_id','building_name']
        buildings = [dict(zip(columns_buildings, row)) for row in buildings]

        return render(request, 'asset_management/enclosure/edit_enclosure.html', {'enclosures': enclosures,'buildings' :buildings})

    if request.method == 'POST':
        current_enclosure_number = request.POST.get('current_enclosure_number')
        building_id = request.POST.get('building_id')
        square_foot = request.POST.get('square_foot')
        enclosure_number = request.POST.get('enclosure_number')

        query = "UPDATE enclosure SET square_foot = %s, enclosure_number = %s, building_id =%s WHERE enclosure_number = %s;"
        success = execute_query(query, square_foot, enclosure_number, building_id, current_enclosure_number, query_type="UPDATE")

        if success:
            messages.success(request, "Enclosure updated successfully.")
            return redirect('enclosure_actions')
        else:
            messages.error(request, "There was an error updating the enclosure.")

    return render(request, 'asset_management/enclosure/edit_enclosure.html', {'enclosure': success})

def delete_enclosure(request, enclosure_number):
    if request.method == 'POST':
        query = "DELETE FROM enclosure WHERE enclosure_number = %s;"
        success = execute_query(query, enclosure_number, query_type="DELETE")
        
    return redirect('enclosure_actions')

######################################################
#                    show
######################################################

def show_actions(request):
    query = '''SELECT s.show_id, s.attraction_id, a.attraction_name, s.tickets_sold, s.status, s."date", s."Time", s.revenue
    FROM "show" s JOIN attraction a ON s.attraction_id = a.attraction_id;'''
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load shows.")
        return render(request, 'error.html')

    columns_show = ['show_id', 'attraction_id', 'attraction_name', 'tickets_sold', 'status', 'date', 'time', 'revenue']
    shows = [dict(zip(columns_show, row)) for row in results]

    return render(request, 'asset_management/show/show_actions.html', {'shows': shows})

def add_show(request):
    if request.method == 'GET':
        # Fetch attraction from the database
        query = "SELECT attraction_id, attraction_name FROM attraction;"
        attraction, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_attractions = ['attraction_id','attraction_name']
        attractions = [dict(zip(columns_attractions, row)) for row in attraction]
        
        return render(request, 'asset_management/show/add_show.html', {'attractions':attractions})
    
    if request.method == 'POST':
        # Fetch data from form
        attraction_id = request.POST.get('attraction_id')
        tickets_sold = request.POST.get('tickets_sold')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        revenue = request.POST.get('revenue')
        
        
        # SQL query to insert new show
        query = "INSERT INTO show (attraction_id, tickets_sold, status,date,\"Time\", revenue) VALUES (%s, %s, %s, %s, %s, %s);"
        success = execute_query(query, attraction_id, tickets_sold, status, date, time, revenue, query_type="INSERT")

        if success:
            messages.success(request, "New show added successfully.")
            return redirect('show_actions')
        else:
            messages.error(request, "There was an error adding the show.")

    return render(request, 'asset_management/show/add_show.html')

def edit_show(request, show_id):
    if request.method == 'GET':
        query = '''SELECT s.show_id, s.attraction_id, a.attraction_name, s.tickets_sold, s.status, s."date", s."Time", s.revenue
        FROM "show" s JOIN attraction a ON s.attraction_id = a.attraction_id WHERE show_id = %s ;'''
        results, success = execute_query(query,show_id, query_type='SELECT')

        if not success:
            messages.error(request, "Failed to load shows.")
            return render(request, 'error.html')

        columns_show = ['show_id', 'attraction_id', 'attraction_name', 'tickets_sold', 'status', 'date', 'time', 'revenue']
        shows = [dict(zip(columns_show, row)) for row in results]

        # # Fetch attraction from the database
        # query = "SELECT attraction_id, attraction_name FROM attraction;"
        # attraction, success = execute_query(query, query_type="SELECT")
        
        # if not success:
        #     messages.error(request, 'Failed to fetch employee types!')
        #     return render(request, 'error.html')

        # columns_attractions = ['attraction_id','attraction_name']
        # attractions = [dict(zip(columns_attractions, row)) for row in attraction]
        
        return render(request, 'asset_management/show/edit_show.html', {'shows': shows})

    if request.method == 'POST':
        tickets_sold = request.POST.get('tickets_sold')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        revenue = request.POST.get('revenue')
        
        query = "UPDATE show SET  tickets_sold = %s, status = %s, date = %s, \"Time\" = %s, revenue = %s WHERE show_id = %s;"
        success = execute_query(query, tickets_sold, status, date, time, revenue, show_id, query_type="UPDATE")

        if success:
            messages.success(request, "Show updated successfully.")
            return redirect('show_actions')
        else:
            messages.error(request, "There was an error updating the show.")

    return render(request, 'asset_management/show/edit_show.html')

def delete_show(request, show_id):
    if request.method == 'POST':
        # SQL query to delete the show
        query = "DELETE FROM \"show\" WHERE show_id = %s;"
        success = execute_query(query, show_id, query_type="DELETE")
        
        if success:
            messages.success(request, "Show deleted successfully.")
        else:
            messages.error(request, "There was an error deleting the show.")

    return redirect('show_actions')

######################################################
#                    Product
######################################################

def product_actions(request):
    # SQL query to select all products and the concession they belong to
    query = '''
    SELECT p.product_id, p.product_name, p.price, c.concession_name
    FROM product p
    LEFT JOIN concession_product cp ON p.product_id = cp.product_id
    LEFT JOIN concession c ON cp.concession_id = c.concession_id;
    '''
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load products and their concessions.")
        return render(request, 'error.html')

    # Define column names as they are expected in the results
    columns_product = ['product_id', 'product_name', 'price', 'concession_name']
    products = [dict(zip(columns_product, row)) for row in results]

    # Render the product actions page with the products data
    return render(request, 'asset_management/product/product_actions.html', {'products': products})

def add_product(request):
    if request.method == 'GET':
        # Fetch concession from the database
        query = "SELECT concession_id, concession_name FROM concession;"
        concession, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_concession = ['concession_id','concession_name']
        concessions = [dict(zip(columns_concession, row)) for row in concession]
        
        return render(request, 'asset_management/product/add_product.html', {'concessions':concessions})
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        concession_id = request.POST.get('concession_id')

        query = "INSERT INTO product (product_name, price) VALUES (%s, %s);"
        success = execute_query(query, product_name, price, query_type="INSERT")
        
        query = "SELECT product_id FROM product WHERE product_name =%s; "
        product_id_, success = execute_query(query, product_name, query_type="SELECT")
        product_id = product_id_[0][0]
        
        # If a concession_id was provided, link the product to the concession
        if success and concession_id:
            query = "INSERT INTO concession_product (concession_id, product_id) VALUES (%s, %s);"
            success = execute_query(query, concession_id, product_id, query_type="INSERT")

        if success:
            messages.success(request, "Product added successfully.")
            return redirect('product_actions')
        else:
            messages.error(request, "Failed to add product.")

    # Render the add product form template
    return render(request, 'asset_management/product/add_product.html')

def edit_product(request, product_id):
    if request.method == 'GET':
        # Fetch the product details along with its concession
        query = '''SELECT p.product_id, p.product_name, p.price, c.concession_id, c.concession_name
        FROM product p LEFT JOIN concession_product cp ON p.product_id = cp.product_id
        LEFT JOIN concession c ON cp.concession_id = c.concession_id
        WHERE p.product_id = %s;'''
        product, success = execute_query(query, product_id, query_type='SELECT')

        if not success:
            messages.error(request, "Failed to load product details.")
            return render(request, 'error.html')
        
        columns_product = ['product_id','product_name','price','concession_id','concession_name']
        products = [dict(zip(columns_product, row)) for row in product]
        
        # Fetch concession from the database
        query = "SELECT concession_id, concession_name FROM concession;"
        concession, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_concession = ['concession_id','concession_name']
        concessions = [dict(zip(columns_concession, row)) for row in concession]

        # Render the edit product form template with product details
        return render(request, 'asset_management/product/edit_product.html', {'products': products,'concessions':concessions})

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        concession_id = request.POST.get('concession_id')
        
        query = "UPDATE product SET product_name = %s, price = %s WHERE product_id = %s;"
        success = execute_query(query, product_name, price, product_id, query_type="UPDATE")

        # Update the concession_product link
        if success:
            # First, remove any existing link
            query = "DELETE FROM concession_product WHERE product_id = %s;"
            execute_query(query, product_id, query_type="DELETE")

            # If a concession_id was provided, create a new link
            if concession_id:
                query = "INSERT INTO concession_product (concession_id, product_id) VALUES (%s, %s);"
                success = execute_query(query, concession_id, product_id, query_type="INSERT")

        if success:
            messages.success(request, "Product updated successfully.")
            return redirect('product_actions')
        else:
            messages.error(request, "Failed to update product.")

    # Render the edit product form template
    return render(request, 'asset_management/product//edit_product.html')

def delete_product(request, product_id):
    if request.method == 'POST':
        
        query = "DELETE FROM concession_product WHERE product_id = %s;"
        success = execute_query(query, product_id, query_type="DELETE")

        # Delete the product
        if success:
            query = "DELETE FROM product WHERE product_id = %s;"
            success = execute_query(query, product_id, query_type="DELETE")

        if success:
            messages.success(request, "Product deleted successfully.")
        else:
            messages.error(request, "Failed to delete product.")

    return redirect('product_actions')

######################################################
#                    Species
######################################################
def species_actions(request):
    # SQL query to select all species
    query = "SELECT species_id, species_name, habitat, diet, monthly_food_cost, species_type FROM species;"
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load species.")
        return render(request, 'error.html')

    # Define column names as they appear in the database
    columns_species = ['species_id', 'species_name', 'habitat', 'diet', 'monthly_food_cost', 'species_type']
    species = [dict(zip(columns_species, row)) for row in results]

    # Render the species actions page with the species data
    return render(request, 'asset_management/species/species_actions.html', {'species': species})

def info_species(request, species_id):
    species_type = request.GET.get('species_type')
    query = "SELECT * FROM species WHERE species_id = %s;"
    results, success = execute_query(query, species_id, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load species details.")
        return render(request, 'error.html')
    
    species = []
    columns_species = ['species_id', 'species_name', 'habitat', 'diet', 'monthly_food_cost', 'species_type']
    for row in results:
        species_ = dict(zip(columns_species, row)) 
        species.append(species_)
    
     # Retrieve additional information based species_type
    if species_type == 'Bird':
        bird_info_query = "SELECT feather_type, nesting_behaviour, migratory FROM bird WHERE species_id = %s"
        bird_info_results, _ = execute_query(bird_info_query, species_id, query_type="SELECT")
        columns_bird = ['feather_type','nesting_behaviour','migratory']
        for row in bird_info_results:
            bird_data =dict(zip(columns_bird,row))
            species[0].update(bird_data)
        
    elif species_type == 'Mammal':
        mammal_info_query = "SELECT fur_type, gestation_period FROM mammal WHERE species_id = %s"
        mammal_info_results, _ = execute_query(mammal_info_query, species_id, query_type="SELECT")
        columns_mammal = ['fur_type','gestation_period']
        for row in mammal_info_results:
            mammal_data = dict(zip(columns_mammal,row))
            species[0].update(mammal_data)
        
    elif species_type == 'Reptile':
        reptile_info_query = "SELECT scale_type, temperature_range, venomous FROM reptile WHERE species_id = %s"
        reptile_info_results, _ = execute_query(reptile_info_query, species_id, query_type="SELECT")
        columns_reptile = ['scale_type','temperature_range','venomous']
        for row in reptile_info_results:
            reptile_data = dict(zip(columns_reptile,row))
            species[0].update(reptile_data)
    
    elif species_type == 'Aquatic':
        aquatic_info_query = "SELECT finned_type, average_length FROM aquatic WHERE species_id = %s"

        aquatic_info_results, _ = execute_query(aquatic_info_query, species_id, query_type="SELECT")
        columns_aquatic = ['finned_type','average_length']
        for row in aquatic_info_results:
            aquatic_data = dict(zip(columns_aquatic,row))
            species[0].update(aquatic_data)
    

    return render(request, 'asset_management/species/info_species.html', {'species': species})

def add_species(request):
    if request.method == 'GET':
        # Fetch species from the database
        species_query = "SELECT DISTINCT species_id, species_name,species_type FROM species;"
        species, species_success = execute_query(species_query, query_type="SELECT")

        if not species_success:
            messages.error(request, 'Failed to fetch species!')
            return render(request, 'error.html')

        columns_species = ['species_id', 'species_name','species_type']
        species = [dict(zip(columns_species, row)) for row in species]
        
        return render(request, 'asset_management/species/add_species.html',{'species': species})
        
    if request.method == 'POST':
        species_name = request.POST.get('species_name')
        habitat = request.POST.get('habitat')
        diet = request.POST.get('diet')
        monthly_food_cost = request.POST.get('monthly_food_cost')
        species_type = request.POST.get('species_type')
        
        species_query = "INSERT INTO species (species_name, habitat, diet, monthly_food_cost, species_type) VALUES (%s, %s, %s, %s, %s);"
        success = execute_query(species_query, species_name, habitat, diet, monthly_food_cost, species_type, query_type="INSERT")

        if not success:
            messages.error(request, "There was an error adding the species.")
            return render(request, 'asset_management/species/add_species.html')
        
        else:
            query = "SELECT species_id FROM species WHERE species_name =%s;"
            species_id_,success_ = execute_query(query,species_name,query_type='SELECT') 
            species_id = species_id_[0][0]

            
            # Depending on the species type, insert additional data into the respective table
            if species_type == 'Mammal':
                fur_type = request.POST.get('fur_type')
                gestation_period = request.POST.get('gestation_period')
                mammal_query = "INSERT INTO mammal (species_id, fur_type, gestation_period) VALUES (%s, %s, %s);"
                success = execute_query(mammal_query, species_id, fur_type, gestation_period, query_type="INSERT")

            elif species_type == 'Bird':
                feather_type = request.POST.get('feather_type')
                nesting_behaviour = request.POST.get('nesting_behaviour')
                migratory = request.POST.get('migratory') == 'on'
                bird_query = "INSERT INTO bird (species_id, feather_type, nesting_behaviour, migratory) VALUES (%s, %s, %s, %s);"
                success = execute_query(bird_query, species_id, feather_type, nesting_behaviour, migratory, query_type="INSERT")
                
            elif species_type == 'Reptile':
                scale_type = request.POST.get('scale_type')
                temperature_range = request.POST.get('temperature_range')
                venomous = request.POST.get('venomous') == 'on'
                reptile_query = "INSERT INTO reptile (species_id, scale_type, temperature_range, venomous) VALUES (%s, %s, %s, %s);"
                success = execute_query(reptile_query, species_id, scale_type, temperature_range, venomous, query_type="INSERT")

            elif species_type == 'Aquatic':
                finned_type = request.POST.get('finned_type')
                average_length = request.POST.get('average_length')
                aquatic_query = "INSERT INTO aquatic (species_id, finned_type, average_length) VALUES (%s, %s, %s);"
                success = execute_query(aquatic_query, species_id, finned_type, average_length, query_type="INSERT")

            if not success:
                # If there was an error inserting type-specific data, delete the species entry and rollback the transaction
                delete_query = "DELETE FROM species WHERE species_id = %s;"
                execute_query(delete_query, species_id, query_type="DELETE")
                messages.error(request, "There was an error adding the type-specific data for the species.")
                return render(request, 'asset_management/species/add_species.html')

            messages.success(request, "New species and its type-specific data added successfully.")
            return redirect('species_actions')

    return render(request, 'asset_management/species/add_species.html')

def edit_species(request, species_id):
    if request.method == 'GET':
        query = "SELECT * FROM species WHERE species_id = %s;"
        results, success = execute_query(query, species_id, query_type='SELECT')

        if not success:
            messages.error(request, "Failed to load species details.")
            return render(request, 'error.html')
        
        species = []
        columns_species = ['species_id', 'species_name', 'habitat', 'diet', 'monthly_food_cost', 'species_type']
        for row in results:
            species_ = dict(zip(columns_species, row)) 
            species.append(species_)
        
        # Retrieve additional information based species_type
        
        bird_info_query = "SELECT feather_type, nesting_behaviour, migratory FROM bird WHERE species_id = %s"
        bird_info_results, _ = execute_query(bird_info_query, species_id, query_type="SELECT")
        if not success:
            messages.error(request, "Failed to load species details.")
            return render(request, 'error.html')
        columns_bird = ['feather_type','nesting_behaviour','migratory']
        for row in bird_info_results:
            bird_data =dict(zip(columns_bird,row))
            species[0].update(bird_data)
            
        
        mammal_info_query = "SELECT fur_type, gestation_period FROM mammal WHERE species_id = %s"
        mammal_info_results, _ = execute_query(mammal_info_query, species_id, query_type="SELECT")
        if not success:
            messages.error(request, "Failed to load species details.")
            return render(request, 'error.html')
        columns_mammal = ['fur_type','gestation_period']
        for row in mammal_info_results:
            mammal_data = dict(zip(columns_mammal,row))
            species[0].update(mammal_data)
            
        
        reptile_info_query = "SELECT scale_type, temperature_range, venomous FROM reptile WHERE species_id = %s"
        reptile_info_results, _ = execute_query(reptile_info_query, species_id, query_type="SELECT")
        if not success:
            messages.error(request, "Failed to load species details.")
            return render(request, 'error.html')
        columns_reptile = ['scale_type','temperature_range','venomous']
        for row in reptile_info_results:
            reptile_data = dict(zip(columns_reptile,row))
            species[0].update(reptile_data)
        
        
        aquatic_info_query = "SELECT finned_type, average_length FROM aquatic WHERE species_id = %s"
        aquatic_info_results, _ = execute_query(aquatic_info_query, species_id, query_type="SELECT")
        if not success:
            messages.error(request, "Failed to load species details.")
            return render(request, 'error.html')
        columns_aquatic = ['fin_type','average_length']
        for row in aquatic_info_results:
            aquatic_data = dict(zip(columns_aquatic,row))
            species[0].update(aquatic_data)
    

        return render(request, 'asset_management/species/edit_species.html', {'species': species})

    if request.method == 'POST':
        current_species_type = request.POST.get('current_species_type')
        species_name = request.POST.get('species_name')
        habitat = request.POST.get('habitat')
        diet = request.POST.get('diet')
        monthly_food_cost = request.POST.get('monthly_food_cost')
        species_type = request.POST.get('species_type')

        # Additional attributes
        feather_type = request.POST.get('feather_type')
        nesting_behaviour = request.POST.get('nesting_behaviour')
        migratory = request.POST.get('migratory') == 'on'  # Convert checkbox to boolean
        fur_type = request.POST.get('fur_type')
        gestation_period = request.POST.get('gestation_period')
        scale_type = request.POST.get('scale_type')
        temperature_range = request.POST.get('temperature_range')
        venomous = request.POST.get('venomous') == 'on'  # Convert checkbox to boolean
        finned_type = request.POST.get('finned_type')
        average_length = request.POST.get('average_length')

        query = "UPDATE species SET species_name = %s, habitat = %s, diet = %s, monthly_food_cost = %s, species_type = %s WHERE species_id = %s;"
        success = execute_query(query, species_name, habitat, diet, monthly_food_cost, species_type, species_id, query_type="UPDATE")

        if success:
            def delete_previous_species_type_data(current_species_type):
                # Map species type ID to the respective table and column name
                type_table_map = {
                    'Bird': ('bird', 'species_id'),
                    'Mammal': ('mammal', 'species_id'),
                    'Reptile': ('reptile', 'species_id'),
                    'Aquatic': ('aquatic', 'species_id')
                }
                result = type_table_map.get(current_species_type)
                if result:
                    table, column = result
                    query_delete = f"DELETE FROM {table} WHERE {column} = %s;"
                    execute_query(query_delete, species_id, query_type="DELETE")
                    # Note: Handle exceptions as needed
                else:
                    print(f"No mapping found for species_type_id: {current_species_type}")
                    
            if current_species_type != species_type:
                delete_previous_species_type_data(current_species_type)
                # Insert new species type details
                if species_type == 'Mammal':
                    fur_type = request.POST.get('fur_type')
                    gestation_period = request.POST.get('gestation_period')
                    mammal_query = "INSERT INTO mammal (species_id, fur_type, gestation_period) VALUES (%s, %s, %s);"
                    success = execute_query(mammal_query, species_id, fur_type, gestation_period, query_type="INSERT")

                elif species_type == 'Bird':
                    feather_type = request.POST.get('feather_type')
                    nesting_behaviour = request.POST.get('nesting_behaviour')
                    migratory = request.POST.get('migratory') == 'on'
                    bird_query = "INSERT INTO bird (species_id, feather_type, nesting_behaviour, migratory) VALUES (%s, %s, %s, %s);"
                    success = execute_query(bird_query, species_id, feather_type, nesting_behaviour, migratory, query_type="INSERT")
                    
                elif species_type == 'Reptile':
                    scale_type = request.POST.get('scale_type')
                    temperature_range = request.POST.get('temperature_range')
                    venomous = request.POST.get('venomous') == 'on'
                    reptile_query = "INSERT INTO reptile (species_id, scale_type, temperature_range, venomous) VALUES (%s, %s, %s, %s);"
                    success = execute_query(reptile_query, species_id, scale_type, temperature_range, venomous, query_type="INSERT")

                elif species_type == 'Aquatic':
                    finned_type = request.POST.get('finned_type')
                    average_length = request.POST.get('average_length')
                    aquatic_query = "INSERT INTO aquatic (species_id, finned_type, average_length) VALUES (%s, %s, %s);"
                    success = execute_query(aquatic_query, species_id, finned_type, average_length, query_type="INSERT")
                
                messages.success(request, "Species updated successfully.")
                return redirect('species_actions')

            else:
                if species_type == 'Bird':
                    bird_query = """UPDATE bird SET feather_type = %s, nesting_behaviour = %s,
                        migratory = %s WHERE species_id = %s;"""
                    additional_attributes_success = execute_query(bird_query, feather_type, nesting_behaviour, migratory, species_id, query_type="UPDATE")
                
                elif species_type == 'Mammal':
                    mammal_query = """UPDATE mammal SET fur_type = %s,
                    gestation_period = %s WHERE species_id = %s;"""
                    additional_attributes_success = execute_query(mammal_query, fur_type, gestation_period, species_id, query_type="UPDATE")
                
                elif species_type == 'Reptile':
                    reptile_query = """UPDATE reptile SET scale_type = %s, temperature_range = %s,
                    venomous = %s WHERE species_id = %s;"""
                    additional_attributes_success = execute_query(reptile_query, scale_type, temperature_range, venomous, species_id, query_type="UPDATE")
                
                elif species_type == 'Aquatic':
                    aquatic_query = """UPDATE aquatic SET finned_type = %s,
                        average_length = %s WHERE species_id = %s;"""
                    additional_attributes_success = execute_query(aquatic_query, finned_type, average_length, species_id, query_type="UPDATE")
                    
                messages.success(request, "Species updated successfully.")
                return redirect('species_actions')
            
        else:
            messages.error(request, "There was an error updating the species.")

def delete_species(request, species_id):
    if request.method == 'POST':
            type_tables = ['mammal', 'bird', 'reptile', 'aquatic']
            for table in type_tables:
                delete_related_query = f"DELETE FROM {table} WHERE species_id = %s;"
                execute_query(delete_related_query, species_id, query_type="DELETE")

            # Now, attempt to delete the species
            delete_species_query = "DELETE FROM species WHERE species_id = %s;"
            success = execute_query(delete_species_query, species_id, query_type="DELETE")

            if success:
                messages.success(request, "Species and all related records deleted successfully.")
            else:
                messages.error(request, "There was an error deleting the species.")

    return redirect('species_actions')

######################################################
#                   Hourly Wages
######################################################

def hourly_wages_actions(request):
    # Assuming 'execute_query' is a utility function you've defined to run database queries
    query = "SELECT employee_type_id, employee_type, rate FROM employee_type;"
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load Hourly Wage.")
        return render(request, 'error.html') 
    
    columns_employee_type = ['employee_type_id','employee_type','rate']
    employee_types = [dict(zip(columns_employee_type, row)) for row in results]

    return render(request, 'asset_management/hourly_wages/hourly_wages_actions.html', {'employee_types': employee_types}) 

def add_hourly_wages(request):
    if request.method == 'POST':
        employee_type = request.POST.get('employee_type')
        rate = request.POST.get('rate')
        query = "INSERT INTO employee_type (employee_type,rate) VALUES (%s, %s);"
        success = execute_query(query, employee_type, rate, query_type="INSERT")

        if success:
            messages.success(request, "New Hourly Wage added successfully.")
            return redirect('hourly_wages_actions')
        else:
            messages.error(request, "There was an error adding the Hourly Wage.")

    return render(request, 'asset_management/hourly_wages/add_hourly_wages.html')

def edit_hourly_wages(request, employee_type_id):
    if request.method == 'GET':
        query = '''SELECT employee_type_id, employee_type, rate FROM employee_type WHERE employee_type_id = %s;'''
        results, success = execute_query(query, employee_type_id, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_employee_type = ['employee_type_id','employee_type','rate']
        employee_types = [dict(zip(columns_employee_type, row)) for row in results]

        return render(request, 'asset_management/hourly_wages/edit_hourly_wages.html', {'employee_types':employee_types})
    
    
    if request.method == 'POST':
        employee_type = request.POST.get('employee_type')
        rate = request.POST.get('rate')
        # Assume you have a function execute_query that handles your database interaction
        query = "UPDATE employee_type SET employee_type = %s, rate = %s WHERE employee_type_id = %s;"
        success = execute_query(query, employee_type, rate, employee_type_id, query_type="UPDATE")

        if success:
            messages.success(request, "Hourly Wages updated successfully.")
            return redirect('hourly_wages_actions')
        else:
            messages.error(request, "There was an error updating the Hourly Wages.")

    return render(request, 'asset_management/hourly_wages/edit_hourly_wages.html', {'employee_types':employee_types})

def delete_hourly_wages(request, employee_type_id):
    if request.method == 'POST':
        # Perform the delete operation
        query = "DELETE FROM employee_type WHERE employee_type_id = %s;"
        success = execute_query(query, employee_type_id, query_type="DELETE")
        
        if success:
            messages.success(request, "Hourly Wages deleted successfully.")
            return redirect('hourly_wages_actions')
        else:
            messages.error(request, "There was an error deleting the Hourly Wages.")
            return redirect('hourly_wages_actions')
    
######################################################
#                    Ticket
######################################################

def ticket_actions(request):
    # Assuming 'execute_query' is a utility function you've defined to run database queries
    query = "SELECT ticket.ticket_id, attraction.attraction_name, ticket.price, ticket.ticket_type, ticket.description FROM ticket JOIN attraction ON ticket.attraction_id = attraction.attraction_id;"
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load Ticket information.")
        return render(request, 'error.html') 
    
    columns_ticket = ['ticket_id','attraction_name', 'price', 'ticket_type', 'description']
    tickets = [dict(zip(columns_ticket, row)) for row in results]

    return render(request, 'asset_management/ticket/ticket_actions.html', {'tickets': tickets})

def add_ticket(request):
    if request.method == 'GET':
        # Fetch attraction from the database
        query = "SELECT attraction_id, attraction_name FROM attraction;"
        attraction, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_attractions = ['attraction_id','attraction_name']
        attractions = [dict(zip(columns_attractions, row)) for row in attraction]
        
        return render(request, 'asset_management/ticket/add_ticket.html',{'attractions':attractions})
        
    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        price = request.POST.get('price')
        description = request.POST.get('description')
        attraction_id = request.POST.get('attraction_id')  # Assuming this comes from the form

        query = "INSERT INTO ticket (attraction_id, price, ticket_type, description) VALUES (%s, %s, %s, %s);"
        success = execute_query(query, attraction_id, price, ticket_type, description, query_type="INSERT")

        if success:
            messages.success(request, "New Ticket added successfully.")
            return redirect('ticket_actions')  # Update this to the correct redirect view
        else:
            messages.error(request, "There was an error adding the Ticket.")

    return render(request, 'asset_management/ticket/add_ticket.html')  # Update template path if necessary

def edit_ticket(request, ticket_id):
    if request.method == 'GET':
        # Fetch attraction from the database
        query = "SELECT attraction_id, attraction_name FROM attraction;"
        attraction, success = execute_query(query, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch employee types!')
            return render(request, 'error.html')

        columns_attractions = ['attraction_id','attraction_name']
        attractions = [dict(zip(columns_attractions, row)) for row in attraction]
        
        query = '''SELECT ticket.ticket_id,attraction.attraction_id, attraction.attraction_name, ticket.price, ticket.ticket_type, ticket.description FROM ticket 
        JOIN attraction ON ticket.attraction_id = attraction.attraction_id WHERE ticket.ticket_id = %s;'''
        results, success = execute_query(query, ticket_id, query_type="SELECT")
        
        if not success:
            messages.error(request, 'Failed to fetch ticket details!')
            return render(request, 'error.html')

        columns_ticket = ['ticket_id','attraction_id', 'attraction_name', 'price', 'ticket_type', 'description']
        tickets= [dict(zip(columns_ticket, row)) for row in results]

        return render(request, 'asset_management/ticket/edit_ticket.html', {'tickets': tickets,'attractions':attractions})
    
    if request.method == 'POST':
        attraction_id = request.POST.get('attraction_id')
        price = request.POST.get('price')
        ticket_type = request.POST.get('ticket_type')
        description = request.POST.get('description')

        query = "UPDATE ticket SET attraction_id = %s, price = %s, ticket_type = %s, description = %s WHERE ticket_id = %s;"
        success = execute_query(query, attraction_id, price, ticket_type, description, ticket_id, query_type="UPDATE")

        if success:
            messages.success(request, "Ticket updated successfully.")
            return redirect('ticket_actions')  # Update this to the correct redirect view
        else:
            messages.error(request, "There was an error updating the Ticket.")

    return render(request, 'asset_management/ticket/edit_ticket.html', {'tickets': tickets})

def delete_ticket(request, ticket_id):
    if request.method == 'POST':
        # Perform the delete operation
        query = "DELETE FROM ticket WHERE ticket_id = %s;"
        success = execute_query(query, ticket_id, query_type="DELETE")
        
        if success:
            messages.success(request, "Ticket deleted successfully.")
            return redirect('ticket_actions')  # Update this to the correct redirect view
        else:
            messages.error(request, "There was an error deleting the Ticket.")
            return redirect('ticket_actions')  # Update this to the correct redirect view