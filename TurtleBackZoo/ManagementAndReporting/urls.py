from django.urls import path
from . import views

urlpatterns = [
    path('', views.managementandreporting_home,name='managementandreporting_home'),
    path('asset_management',views.asset_management,name='asset_management'),
    path('daily_zoo_activity',views.daily_zoo_activity,name='daily_zoo_activity'),
    path('management_and_reporting',views.management_and_reporting,name='management_and_reporting'),
    
    
    path('animal_reports/', views.animal_reports, name='animal_reports'),
    path('top_three_attractions/', views.top_three_attractions, name='top_three_attractions'),
    path('five_best_days/', views.five_best_days, name='five_best_days'),
    path('average_revenue/', views.average_revenue, name='average_revenue'),
    path('revenue_by_source/', views.revenue_by_source, name='revenue_by_source'),
    
]
