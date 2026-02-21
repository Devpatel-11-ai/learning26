from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("register/",views.registerUser,name="register"),
    path('employee/', include(('employee.urls', 'employee'), namespace='employee'))

]