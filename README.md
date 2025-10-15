# TurtleBack Zoo Management System

## Project Description

The **TurtleBack Zoo Management System** is a web application built using the Django framework (version 4.2.6) designed to help manage the daily operations, assets, and reporting for a zoo.

The application is structured into four main functional areas:

* **Home/Sales**: Provides the main landing page and modules for processing sales transactions for both attractions and concessions.
* **Asset Management**: Allows for the management of the zoo's physical and organizational assets.
* **Daily Zoo Activity**: Provides a view of daily transactions and attendance data.
* **Reports**: Generates key management reports for decision-making.

## Features

The core features of the system include:

### 1. Asset Management
* **Building** management (add, edit, delete buildings).
* **Employee** and **Hourly Wages** management.
* **Attractions** and **Shows** management, including species requirements for attractions.
* **Concessions** and **Product** management.
* **Animal**, **Enclosure**, **Species**, and **Ticket** management.

### 2. Sales
* **Attraction Ticket Sales**: Process sales for specific shows and ticket types (Adult, Child, Senior Entry).
* **Concession Sales**: Process sales for various products under different concessions.

### 3. Reporting and Analytics
* Generate reports on **Animal Population by Species**.
* Identify the **Top Three Attractions** by revenue within a date range.
* Identify the **5 Best Days** by total revenue for a selected month.
* Calculate **Average Revenue** for attractions and concessions.
* Report **Revenue by Source** (Attractions vs. Concessions) for a selected date.

## Prerequisites

To run this project, you need the following installed:

* **Python 3.x**
* **PostgreSQL Database Server**

## Installation and Setup

Follow these steps to get the project running locally.

### 1. Database Setup

The application is configured to use a PostgreSQL database.

* Create a PostgreSQL database named `TurtleBackZoo`.
* The application's connection settings are configured as follows:
    * **Database Name**: `TurtleBackZoo`
    * **User**: `postgres`
    * **Password**: `root1234`
    * **Host**: `localhost`

### 2. Project Dependencies

Navigate to the project's root directory (the one containing `manage.py`) and install the required Python packages:

```bash
pip install -r requirements.txt
```
Key dependencies include Django (4.2.6) and psycopg2 for PostgreSQL connectivity.

3. Run Migrations
Apply the database schema changes using Django's migration commands.

```bash
python manage.py makemigrations
python manage.py migrate
```

Running the Application
Start the Django development server:

```bash
python manage.py runserver
```

Once the server is running, access the application in your web browser at: http://127.0.0.1:8000/


4. Images
<img width="1890" height="910" alt="Screenshot 2025-10-15 164324" src="https://github.com/user-attachments/assets/32622879-3d86-492e-aaa9-b64db8244b4d" />
<img width="1909" height="908" alt="Screenshot 2025-10-15 164313" src="https://github.com/user-attachments/assets/78d7ac8a-8b3b-4d87-ad89-81232e652a04" />
<img width="1897" height="907" alt="Screenshot 2025-10-15 164302" src="https://github.com/user-attachments/assets/08381648-d711-418b-a0ba-a352656b9f24" />
<img width="1917" height="909" alt="Screenshot 2025-10-15 164251" src="https://github.com/user-attachments/assets/750201b7-1049-4874-be17-11ccfcb2279d" />
<img width="1916" height="911" alt="Screenshot 2025-10-15 164245" src="https://github.com/user-attachments/assets/a2243505-d5e8-4afc-847a-852df0a266f8" />
<img width="1918" height="914" alt="Screenshot 2025-10-15 164155" src="https://github.com/user-attachments/assets/613533bc-440d-4442-a4d7-4911b1215f98" />
<img width="1892" height="911" alt="Screenshot 2025-10-15 164353" src="https://github.com/user-attachments/assets/5ff35836-980c-4fe0-8155-ec8bb3633040" />

