from django.shortcuts import render

# Create your views here.

def studentHome(request):
    return render(request,"studentHome.html")
def studentDashboard(request):
    student = {"name":"Dev","age":21,"city":"Ahmedabad"}
    return render(request,"student/studentDashboard.html",student)    
    #student/studentDashboard.html
    #folder/filename

def studentmarks(request):
    marks = {"Yaksh":99,"Jeel":95,"Om":97}
    return render(request,"student/studentmarks.html",marks)    

def studentid(request):
    id = {"Yaksh":101,"Jeel":102,"Om":103}
    return render(request,"student/studentid.html",id)    