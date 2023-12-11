from django import template
from django.db import connection
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



def managementandreporting_home(request):
    return render(request,'home.html',{'name':'managementandreporting_home'})

def animal_reports(request):
    query = '''
        SELECT 
            sp.species_name,
            COUNT(CASE WHEN an.status = 'Healthy' THEN 1 ELSE NULL END) AS number_healthy,
            COUNT(CASE WHEN an.status = 'Medical Care' THEN 1 ELSE NULL END) AS number_medical_care,
            COUNT(CASE WHEN an.status = 'Maternal Leave' THEN 1 ELSE NULL END) AS maternal_leave,
            COUNT(CASE WHEN an.status = 'New Born' THEN 1 ELSE NULL END) AS number_newborn,
            sp.monthly_food_cost AS monthly_cost,
            sp.monthly_food_cost * (
                COUNT(CASE WHEN an.status = 'Healthy' THEN 1 END) + 
                COUNT(CASE WHEN an.status = 'Medical Care' THEN 1 END) + 
                COUNT(CASE WHEN an.status = 'Maternal Leave' THEN 1 END) + 
                COUNT(CASE WHEN an.status = 'New Born' THEN 1 END)
            ) AS total_monthly_food_cost,
            COUNT(DISTINCT vet.employee_id) AS number_of_vets,
            COUNT(DISTINCT acs.employee_id) AS number_of_care_staff
        FROM 
            species sp
        LEFT JOIN 
            animals an ON sp.species_id = an.species_id
        LEFT JOIN 
            veterinarian vet ON sp.species_id = vet.species_id
        LEFT JOIN 
            animal_care_trainer_and_specialist acs ON sp.species_id = acs.species_id
        LEFT JOIN 
            employee e ON vet.employee_id = e.employee_id OR acs.employee_id = e.employee_id
        LEFT JOIN 
            employee_type et ON e.employee_type_id = et.employee_type_id
        GROUP BY 
            sp.species_name, sp.monthly_food_cost
        ORDER BY 
            sp.species_name;
        '''

    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load information.")
        return render(request, 'error.html') 
    
    columns_ = ['species_name','number_healthy', 'number_medical_care', 'maternal_leave', 'number_newborn','monthly_cost',
                 'total_monthly_food_cost' ,'number_of_vets','total_vet_cost']
    
    species = [dict(zip(columns_, row)) for row in results]

    
    return render(request,'management_and_reporting/animal_reports.html',{'species':species})

def top_three_attractions(request):
    if request.method == 'GET':
        return render(request, 'management_and_reporting/top_three_attractions.html')
     
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Ensure both dates are provided
        if not start_date or not end_date:
            messages.error(request, "Please provide both start and end dates.")
            return render(request, 'management_and_reporting/top_three_attractions.html')

        query = '''
            SELECT a.attraction_name, SUM(s.revenue) AS total_revenue
            FROM 
                "show" s
            INNER JOIN 
                attraction a ON s.attraction_id = a.attraction_id
            WHERE 
                s."date" BETWEEN %s AND %s 
            GROUP BY 
                a.attraction_name
            ORDER BY 
                total_revenue DESC
            LIMIT 3;
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [start_date, end_date])
                rows = cursor.fetchall()
            columns = ['attraction_name', 'total_revenue']
            top_three_attractions = [dict(zip(columns, row)) for row in rows]

            return render(request, 'management_and_reporting/top_three_attractions.html', {'top_three_attractions': top_three_attractions})

        except Exception as e:
            messages.error(request, f"Failed to load information due to: {str(e)}")
            return render(request, 'error.html')


    return render(request,'management_and_reporting/top_three_attractions.html',{'top_three_attractions':top_three_attractions})


def five_best_days(request):
    if request.method == 'GET':
        return render(request, 'management_and_reporting/five_best_days.html')
     
    if request.method == 'POST':
        month_number = request.POST.get('month_number')  # You can make the month number dynamic based on user input

        if not month_number:
            messages.error(request, "Please select a month.")
            return render(request, 'management_and_reporting/five_best_days.html')

        query = '''
            SELECT 
                DATE_TRUNC('day', s."date") AS show_date,
                SUM(s.revenue) AS total_revenue
            FROM 
                "show" s
            WHERE 
                EXTRACT(MONTH FROM s."date") = %s
            GROUP BY 
                show_date
            ORDER BY 
                total_revenue DESC
            LIMIT 5;
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [month_number])
                rows = cursor.fetchall()
            columns = ['show_date', 'total_revenue']
            top_shows = [dict(zip(columns, row)) for row in rows]

            return render(request, 'management_and_reporting/five_best_days.html', {'top_shows': top_shows})

        except Exception as e:
            messages.error(request, f"Failed to load information due to: {str(e)}")
            return render(request, 'error.html')

    return render(request, 'management_and_reporting/five_best_days.html')

def average_revenue(request):
    query = ''' SELECT a.attraction_name, AVG(s.revenue) AS average_revenue 
    FROM attraction a INNER JOIN "show" s ON a.attraction_id = s.attraction_id GROUP BY a.attraction_name; '''
    
    results, success = execute_query(query, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load information.")
        return render(request, 'error.html') 
    columns_ = ['attraction_name','average_revenue']
    attraction_revenues = [dict(zip(columns_, row)) for row in results]
    
    query_concession_revenues = '''SELECT c.concession_name, 
    AVG(tr.unit_price) AS concession_price
    FROM concession c
    INNER JOIN transaction_concession tc ON c.concession_id = tc.concession_id
    INNER JOIN transaction tr ON tc.transaction_id = tr.transaction_id
    GROUP BY c.concession_name;'''
    results_concession_revenues, success_concession_revenues = execute_query(query_concession_revenues, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load information.")
        return render(request, 'error.html') 
    columns_concession_revenues = ['concession_name','concession_price']
    concession_revenues = [dict(zip(columns_concession_revenues, row)) for row in results_concession_revenues]
    
    query_total_attendance = ''' SELECT 
    a.attraction_name || ' - ' || TO_CHAR(s."date", 'YYYY-MM-DD') || ' ' || TO_CHAR(s."Time", 'HH24:MI') AS show_name,
    s.tickets_sold AS total_attendance
    FROM "show" s
    INNER JOIN attraction a ON s.attraction_id = a.attraction_id
    ORDER BY s."date", s."Time";'''
    results_total_attendance, success_total_attendance = execute_query(query_total_attendance, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load information.")
        return render(request, 'error.html') 
    columns_total_attendance = ['show_name','total_attendance']
    total_attendance = [dict(zip(columns_total_attendance, row)) for row in results_total_attendance]
    
    context = {
            'attraction_revenues': attraction_revenues,
            'concession_revenues':concession_revenues,
            'total_attendance': total_attendance
        }

    return render(request, 'management_and_reporting/average_revenue.html',context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]




    
   

def revenue_by_source(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')

        # Fetching total revenue for attractions
        query_attractions = '''
            SELECT 
                a.attraction_id, 
                a.attraction_name, 
                COALESCE(SUM(s.revenue), 0) AS total_revenue
            FROM 
                attraction a
            LEFT JOIN 
                "show" s ON a.attraction_id = s.attraction_id
            WHERE 
                s."date" = %s
            GROUP BY 
                a.attraction_id, a.attraction_name;
        '''
        attractions, success_attractions = execute_query(query_attractions, selected_date, query_type="SELECT")

        # Fetching revenue from concessions
        query_concessions = '''
            SELECT 
            c.concession_name, 
            COALESCE(SUM(t.ncount * t.unit_price), 0) AS total_revenue
        FROM 
            concession c
        LEFT JOIN 
            transaction_concession tc ON c.concession_id = tc.concession_id
        LEFT JOIN 
            "transaction" t ON tc.transaction_id = t.transaction_id
        WHERE 
            t.time_stamp::date = %s 
        GROUP BY 
            c.concession_name;

        '''
        concessions, success_concessions = execute_query(query_concessions, selected_date, query_type="SELECT")

        if success_attractions and success_concessions:
            return render(request, 'management_and_reporting/revenue_by_source.html', {
                'selected_date': selected_date, 
                'attractions': attractions,
                'concessions': concessions 
            })
        else:
            # Handle database query failure
            error_message = "Failed to fetch revenue data from the database."
            return render(request, 'error.html', {'error_message': error_message})

    
    return render(request,'management_and_reporting/revenue_by_source.html')
