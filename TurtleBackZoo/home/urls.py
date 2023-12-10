from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('asset_management',views.asset_management,name='asset_management'),
    path('daily_zoo_activity',views.daily_zoo_activity,name='daily_zoo_activity'),
    path('management_and_reporting',views.management_and_reporting,name='management_and_reporting'),

    #sale
    path('sale_home/', views.sale_home, name='sale_home'),

    path('attraction_sale/', views.attraction_sale, name='attraction_sale'),
    path('shows_attraction_sale/', views.shows_attraction_sale, name='shows_attraction_sale'),


    path('process_transaction/', views.process_transaction, name='process_transaction'),

    
    path('concession_sale/', views.concession_sale, name='concession_sale'), 
    path('menu_concession_sale/', views.menu_concession_sale, name='menu_concession_sale'),


]
