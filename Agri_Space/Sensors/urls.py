from django.urls import path
from . import views

urlpatterns = [
    path('relay-control/', views.relay_control, name='relay_control'), 
    path('water-usage-individual/', views.water_usage, name='water_usage'), 
    path('total-water-usage/', views.total_water_usage, name='total_water_usage'), 
    path('relay-state-operations/<int:id>/', views.relay_state, name='relay_state'), 
    path('irrigation-cycle-operations/<int:id>/', views.irrigation_cycle, name='irrigation_cycle'), 
]