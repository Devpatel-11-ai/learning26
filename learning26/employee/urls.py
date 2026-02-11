
from . import views
from django.urls import path
urlpatterns = [
    path('employeeList/', views.employeeList),
    path('employeeFilter/', views.employeeFilter),
    path('createEmployee/', views.createEmployee),
     path('createEmployeeWithForm/',views.createEmployeeWithForm),
    path('createCourse/',views.createCourse)
]