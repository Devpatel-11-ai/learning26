from django.urls import path
from . import views

urlpatterns = [
   path("home/",views.studentHome),
   path("dashboard/",views.studentDashboard),
   path("marks/",views.studentmarks),
   path("id/",views.studentid),
   path("serviceList/",views.serviceList,name="serviceList"),
   path("createService/",views.createService,name="createService"),
]