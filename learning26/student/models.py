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

    def __str__(self):
        return self.studentName

class Product(models.Model):
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField()
    productDescription = models.TextField()
    productStock = models.PositiveIntegerField()
    productColor = models.CharField(max_length=20,null=True)
    productStatus = models.BooleanField(default=True)
    
    class Meta:
        db_table = "product"

                 
class StudentProfile(models.Model):
    hobbies =(("reading","reading"),("travel","travel"),("music","music"))
    #studentPrilfe id --> pk create auto...
    studentId = models.OneToOneField(Student,on_delete=models.CASCADE)
    studentHobbies = models.CharField(max_length=100,choices=hobbies)
    studentAddress = models.CharField(max_length=100)
    studentPhone = models.CharField(max_length=10)
    studentGender = models.CharField(max_length=10)
    studentDOB = models.DateField()
    
    class Meta:
        db_table = "studentprofile"

    def __str__(self):
        return self.studentId.studentName

#cat --> #service

class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryDescription = models.TextField()
    categoryStatus = models.BooleanField(default=True)
    
    class Meta:
        db_table = "category"

    def __str__(self):
        return self.categoryName    

class Service(models.Model):
    serviceName = models.CharField(max_length=100)
    serviceDescription = models.TextField()
    servicePrice = models.IntegerField()
    serviceStatus = models.BooleanField(default=True)
    #after table creation adding new field
    discount = models.IntegerField(null=True)
    categoryId = models.ForeignKey(Category,on_delete=models.CASCADE)

    
    class Meta:
        db_table = "service"

    def __str__(self):
        return self.serviceName    

class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    bookingDate = models.DateField()
    bookingTime = models.TimeField()

    class Meta:
        db_table = "booking"

    def __str__(self):
        return str(self.bookingId)

class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    paymentAmount = models.FloatField()
    paymentDate = models.DateField()
    paymentMethod = models.CharField(max_length=50)
    bookingId = models.OneToOneField(Booking,on_delete=models.CASCADE)

    class Meta:
        db_table = "payment"

    def __str__(self):
        return str(self.paymentId)


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    orderDate = models.DateField()
    orderTotal = models.FloatField()

    class Meta:
        db_table = "order"

    def __str__(self):
        return str(self.orderId)

class Inventory(models.Model):
    inventoryId = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    lastUpdated = models.DateField()

    class Meta:
        db_table = "inventory"

    def __str__(self):
        return str(self.inventoryId)        

