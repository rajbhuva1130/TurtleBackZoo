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


def dailyzooacitvity_home(request):

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        query = '''SELECT tr.*, 
        a.attraction_name || ' - ' || TO_CHAR(sh."date", 'YYYY-MM-DD') || ' ' || TO_CHAR(sh."Time", 'HH24:MI') AS show_name
        FROM 
            transaction tr
        INNER JOIN 
            transaction_attraction ta ON tr.transaction_id = ta.transaction_id
        INNER JOIN 
            "show" sh ON ta.show_id = sh.show_id
        INNER JOIN 
            attraction a ON sh.attraction_id = a.attraction_id
        WHERE 
            DATE(tr.time_stamp) = %s;'''
    results, success = execute_query(query,selected_date, query_type='SELECT')

    if not success:
        messages.error(request, "Failed to load information.")
        return render(request, 'error.html') 
    columns = ['transaction_id','employee_id','time_stamp','unit_price','ncount','transaction_type','show_name']
    daily_zoo = [dict(zip(columns, row)) for row in results]
        
    return render(request, 'daily_zoo_activity/daily_home.html', {'daily_zoo':daily_zoo})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]