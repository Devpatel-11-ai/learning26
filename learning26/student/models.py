from django.db import models

# Create your models here.
#python class

#parent class model
#create table student(stydentName varchar(100)),studentAge int,studentCity char
#it  will generate pk automatically
class Student(models.Model):
    studentName= models.CharField(max_length=100)
    studentAge = models.IntegerField()
    studentCity = models.CharField(max_length=40)
    studentEmail = models.EmailField(null=True)
    studentactivate = models.BooleanField(default=True)

    #meta class
    class Meta:
        db_table = "student" #table name

class Product(models.Model):
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField()
    productDescription = models.TextField()
    productStock = models.PositiveIntegerField()
    productColor = models.CharField(max_length=20,null=True)
    productStatus = models.BooleanField(default=True)
    
    class Meta:
        db_table = "product"

class Iteams(models.Model):
    iteamName = models.CharField(max_length=100)
    iteamPrice = models.IntegerField()
    iteamDescription = models.TextField()
    iteamStock = models.PositiveIntegerField()
    iteamColor = models.CharField(max_length=20,null=True)
    iteamStatus = models.BooleanField(default=True)

    class Meta:
        db_table = "iteams"