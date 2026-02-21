from . import views
from django.urls import path
from django.urls import include
app_name = 'employee'
urlpatterns = [
    path('employeeList/', views.employeeList, name='employeeList'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employeeFilter/', views.employeeFilter),
    path('createEmployee/', views.createEmployee),
    path('createEmployeeWithForm/',views.createEmployeeWithForm,name="createEmployeeWithForm"),
    path('createCourse/',views.createCourse),
    path('Department/',views.DepartmentWithForm),
    # path('deleteEmployee/',views.deleteEmployee,name="deleteEmployee")
    path("deleteEmployee/<int:id>",views.deleteEmployee,name="deleteEmployee"),
    path("filterEmployee/",views.filterEmployee,name="filterEmployee"),
    path("sortEmployee/<int:id>",views.sortEmployee,name="sortEmployee"),
    path("updateemployee/<int:id>",views.updateEmployee,name="updateEmployee"),
    path('profile/', views.employee_profile, name='employee_profile'),
    path('jobs/', views.employee_jobs, name='employee_jobs'),
    path('schedule/', views.employee_schedule, name='employee_schedule'),
    path('logout/', views.employee_logout, name='employee_logout'),

    
]