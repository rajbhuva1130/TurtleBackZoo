from django.urls import path
from . import views

urlpatterns = [
    path('', views.managementandreporting_home,name='managementandreporting_home'),
]
