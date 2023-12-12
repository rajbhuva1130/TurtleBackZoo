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
        a.attraction_name || ' - ' || TO_CHAR(sh."date", 'YYYY-MM-DD') || ' ' || TO_CHAR(sh."Time", 'HH24:MI') AS show_name,
        (tr.ncount * tr.unit_price) AS total_cost
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
        columns = ['transaction_id','employee_id','time_stamp','unit_price','ncount','transaction_type','show_name','total_cost']
        daily_zoo = [dict(zip(columns, row)) for row in results]
        
        query_con = '''SELECT tc.*, t.time_stamp, t.unit_price, t.ncount, t.transaction_type, 
        c.concession_name, p.product_name, 
        (t.ncount * t.unit_price) AS total_cost
        FROM transaction_concession tc
        JOIN transaction t ON tc.transaction_id = t.transaction_id
        JOIN concession c ON tc.concession_id = c.concession_id
        JOIN product p ON tc.product_id = p.product_id
        WHERE DATE(t.time_stamp) = %s;'''
        results_con, success_con = execute_query(query_con,selected_date,query_type='SELECT')
        
        columns_con = ['transaction_id','concession_id','product_id','time_stamp','unit_price','ncount','transaction_type','concession_name','product_name','total_cost']
        daily_zoo_con = [dict(zip(columns_con, row)) for row in results_con]
        
        
    return render(request, 'daily_zoo_activity/daily_home.html', {'daily_zoo':daily_zoo,'daily_zoo_con':daily_zoo_con})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]