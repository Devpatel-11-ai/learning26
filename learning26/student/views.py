from django.shortcuts import render

# Create your views here.

def studentHome(request):
    return render(request,"studentHome.html")
def studentDashboard(request):
    student = {"name":"Dev","age":21,"city":"Ahmedabad"}
    return render(request,"student/studentDashboard.html",student)    
    #student/studentDashboard.html
    #folder/filename