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
    
    return render(request,'management_and_reporting/top_three_attractions.html')


def five_best_days(request):
    
    return render(request,'management_and_reporting/five_best_days.html')


def average_revenue(request):
    
    return render(request,'management_and_reporting/average_revenue.html')


def revenue_by_source(request):
    
    return render(request,'management_and_reporting/revenue_by_source.html')