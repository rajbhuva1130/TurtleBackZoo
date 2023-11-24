from django.urls import path
from . import views

urlpatterns = [
    path('', views.dailyzooacitvity_home,name='dailyzooacitvity_home'),
]
