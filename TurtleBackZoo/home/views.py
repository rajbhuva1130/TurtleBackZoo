from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .database_connector import execute_query
import json


# Create your views here.

###################################### Navigation URLS 

def asset_management(request):
    return render(request, 'asset_management/asset_home.html')

def daily_zoo_activity(request):
    return render(request, 'daily_zoo_activity/daily_home.html')

def management_and_reporting(request):
    return render(request, 'management_and_reporting/reports_home.html')

######################################################


def home(request):
    return render(request,'home.html',{'name':'Monil'})

def sale_home(request):
    return render(request, 'sales/sale_home.html')

def attraction_sale(request):
    query = "SELECT  attraction_id, attraction_name, seats FROM attraction;"  # Replace 'attraction' with your attraction table name
    results, success = execute_query(query, query_type="SELECT")

    if success:
        columns = ['attraction_id', 'attraction_name','seats']  # Define column names for reference, add more columns as needed
        
        # Restructuring the data for easier access in the template
        attractions = []
        for row in results:
            attraction = dict(zip(columns, row))  # Creating a dictionary for each row
            attractions.append(attraction)
        
        return render(request, 'sales/attraction_sale.html', {'attractions': attractions})
    else:
        return render(request, 'error.html')


def shows_attraction_sale(request):
    if request.method == 'POST':
        attraction_id = request.POST.get('attraction_id')
        
        # Fetch shows for the given attraction where status is 'open' using execute_query
        show_query = """
            SELECT show_id,date, \"Time\", (attraction.seats - show.tickets_sold) AS available_tickets 
            FROM show
            JOIN attraction ON show.attraction_id = attraction.attraction_id
            WHERE show.attraction_id = %s AND show.status = 'Open';
        """
        show_results, show_success  = execute_query(show_query,attraction_id, query_type="SELECT")
        
        if show_success :
            show_details = [{'show_id' : row[0] ,'date': row[1], 'time': row[2], 'available_tickets': row[3]} for row in show_results]
            ticket_query = """
                SELECT ticket_id, ticket_type, price 
                FROM ticket 
                WHERE attraction_id = %s;
            """
            ticket_results, ticket_success = execute_query(ticket_query, attraction_id, query_type="SELECT")
            
            if ticket_success:
                tickets = [{'ticket_id': row[0], 'ticket_type': row[1], 'price': row[2]} for row in ticket_results]
                return render(request, 'sales/shows_attraction_sale.html', {'show_details': show_details, 'attraction_id': attraction_id, 'tickets': tickets})
            else:
                return render(request, 'error.html')
        else:
            return render(request, 'error.html')
    else:
        return render(request, 'error.html')

def process_transaction(request):
    if request.method == 'POST':    
        transaction_type = request.POST.get('transaction_type')
        employee_id = '262da5c9-4ee9-4cb2-9d6e-0025e98941e8'
        
        if transaction_type == 'Attraction' :
            selected_show_id = request.POST.get('selected_show_id')  # Get selected show ID
            # Loop through POST data to retrieve ticket quantities
            for key, value in request.POST.items():
                
                if key.startswith('ticket_'):
                    ticket_id = key.split('_')[1]  # Extract ticket ID from the key
                    ticket_price = key.split('_')[2]
                    ticket_quantity = value
                    if ticket_quantity > 0 :
                        query_insert_transaction = "INSERT into transaction (employee_id,unit_price,ncount,transaction_type) VALUES (%s, %s, %s, %s) RETURNING transaction_id"
                        transaction_id , success = execute_query(query_insert_transaction, employee_id, ticket_price, ticket_quantity,transaction_type, query_type="INSERT")
                        query_insert_transaction_attraction = "INSERT into transaction_attraction (transaction_id,show_id,ticket_id) VALUES (%s, %s, %s) RETURNING transaction_id "
                        success = execute_query(query_insert_transaction_attraction, transaction_id, selected_show_id, ticket_id, query_type="INSERT")


        elif transaction_type == 'Concession':
                concession_id = request.POST.get('concession_id')  # Retrieve concession ID

                for key, value in request.POST.items():

                    if key.startswith('product_'):
                        product_id = key.split('_')[1]  # Extract product ID from the key
                        product_price = key.split('_')[2]
                        product_quantity = int(value)  # Quantity of the purchased product
                        
                        if product_quantity > 0:
                            # Insert transaction record for the concession product
                            query_insert_transaction = "INSERT INTO transaction (employee_id, unit_price, ncount, transaction_type) VALUES (%s, %s, %s, %s) RETURNING transaction_id"
                            transaction_id, success = execute_query(query_insert_transaction, employee_id, product_price, product_quantity, transaction_type, query_type="INSERT")
                            
                            # Insert transaction details for the concession product
                            query_insert_transaction_concession = "INSERT INTO transaction_concession (transaction_id, concession_id, product_id) VALUES (%s, %s, %s) RETURNING transaction_id"
                            success = execute_query(query_insert_transaction_concession, transaction_id, concession_id, product_id, query_type="INSERT")
        
        return render(request,'home.html')
        # return HttpResponse("Transaction processed successfully!")
    
    return HttpResponse("Invalid request or processing failed.")


def concession_sale(request):
    query = "SELECT concession_id, concession_name FROM concession"
    rows, success = execute_query(query, query_type="SELECT")

    if success:
        concessions = [{'concession_id': row[0], 'concession_name': row[1]} for row in rows]
        return render(request, 'sales/concession_sale.html', {'concessions': concessions})
    else:
        # Handle database query failure
        error_message = "Failed to fetch concessions from the database."
        return render(request, 'error.html', {'error_message': error_message})
    # return render(request, 'concession_sale.html')

def menu_concession_sale(request):
    if request.method == 'POST':
        if 'concession_id' in request.POST:
            concession_id = request.POST['concession_id']

            # Fetch concession products related to the given concession ID
            query = """
                SELECT product.product_id, product.product_name, product.price 
                FROM concession_product 
                JOIN product ON concession_product.product_id = product.product_id 
                WHERE concession_product.concession_id = %s;
            """
            results, success = execute_query(query,concession_id, query_type="SELECT")
            
            if success:
                products = [{'product_id': row[0], 'product_name': row[1], 'price': row[2]} for row in results]
                return render(request, 'sales/menu_concession_sale.html', {'concession_id': concession_id, 'products': products})
    
    return render(request, 'error.html')