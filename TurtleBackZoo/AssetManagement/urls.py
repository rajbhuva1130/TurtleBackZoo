from django.urls import path
from . import views

urlpatterns = [
    path('', views.assetmanagement_home,name='assetmanagement_home'),
]
