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
        
        query = '''
        SELECT 
    a.attraction_name || ' - ' || TO_CHAR(sh."date", 'YYYY-MM-DD') || ' ' || TO_CHAR(sh."Time", 'HH24:MI') AS show_name,
    SUM(tr.ncount) AS total_ncount,
    SUM(tr.ncount * tr.unit_price) AS total_cost
    FROM 
        transaction tr
    INNER JOIN 
        transaction_attraction ta ON tr.transaction_id = ta.transaction_id
    INNER JOIN 
        "show" sh ON ta.show_id = sh.show_id
    INNER JOIN 
        attraction a ON sh.attraction_id = a.attraction_id
    WHERE 
        DATE(tr.time_stamp) = %s
    GROUP BY 
        show_name, a.attraction_name, sh."date", sh."Time";
                '''
        results, success = execute_query(query,selected_date, query_type='SELECT')
        columns = ['show_name','ncount','total_cost']
        daily_zoo = [dict(zip(columns, row)) for row in results]
        
        query_con = '''SELECT 
            c.concession_name, 
            SUM(t.ncount * t.unit_price) AS total_cost
        FROM 
            transaction_concession tc
        JOIN 
            transaction t ON tc.transaction_id = t.transaction_id
        JOIN 
            concession c ON tc.concession_id = c.concession_id
        JOIN 
            product p ON tc.product_id = p.product_id
        WHERE 
            DATE(t.time_stamp) = %s
        GROUP BY 
            c.concession_name; '''
 
        results_con, success_con = execute_query(query_con,selected_date,query_type='SELECT')
        
        columns_con = ['concession_name','total_cost']
        daily_zoo_con = [dict(zip(columns_con, row)) for row in results_con]
        
        query_adult_entry = ''' SELECT SUM(ncount) AS attendance,SUM(unit_price * ncount) AS total_revenue
                                FROM "transaction" t
                                JOIN transaction_attraction ta ON t.transaction_id = ta.transaction_id
                                JOIN ticket ti ON ta.ticket_id = ti.ticket_id
                                WHERE DATE(t.time_stamp) = %s
                                AND ti.ticket_type = 'Adult_Entry';'''

        results_query_adult_entry, success_query_adult_entry = execute_query(query_adult_entry,selected_date,query_type='SELECT')
        columns_adult_entry = ['attendance','revenue']
        daily_adult_entry = [dict(zip(columns_adult_entry, row)) for row in results_query_adult_entry]

        query_child_entry = ''' SELECT SUM(ncount) AS attendance,SUM(unit_price * ncount) AS total_revenue
                                FROM "transaction" t
                                JOIN transaction_attraction ta ON t.transaction_id = ta.transaction_id
                                JOIN ticket ti ON ta.ticket_id = ti.ticket_id
                                WHERE DATE(t.time_stamp) = %s
                                AND ti.ticket_type = 'Child_Entry';'''

        results_query_child_entry, success_query_child_entry = execute_query(query_child_entry,selected_date,query_type='SELECT')
        columns_child_entry = ['attendance','revenue']
        daily_child_entry = [dict(zip(columns_child_entry, row)) for row in results_query_child_entry]

        query_senior_entry = ''' SELECT SUM(ncount) AS attendance,SUM(unit_price * ncount) AS total_revenue
                        FROM "transaction" t
                        JOIN transaction_attraction ta ON t.transaction_id = ta.transaction_id
                        JOIN ticket ti ON ta.ticket_id = ti.ticket_id
                        WHERE DATE(t.time_stamp) = %s
                        AND ti.ticket_type = 'Senior_Entry';'''

        results_query_senior_entry, success_query_senior_entry = execute_query(query_senior_entry,selected_date,query_type='SELECT')
        columns_senior_entry = ['attendance','revenue']
        daily_senior_entry = [dict(zip(columns_senior_entry, row)) for row in results_query_senior_entry]

    return render(request, 'daily_zoo_activity/daily_home.html', {'daily_zoo':daily_zoo,'daily_zoo_con':daily_zoo_con,'daily_adult_entry':daily_adult_entry,'daily_child_entry':daily_child_entry,'daily_senior_entry':daily_senior_entry})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]