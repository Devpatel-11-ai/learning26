from . import views
from django.urls import path
urlpatterns = [
    path("serviceList/",views.servicelist,name="serviceList"),
    path("serviceWithForm/",views.serviceWithForm,name="serviceWithForm"),
    path("deleteservice/<int:id>",views.deleteService,name="deleteService"),
    path("updateService/<int:id>",views.updateService,name="updateService"),
]