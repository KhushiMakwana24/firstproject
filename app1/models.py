from django.db import models
from datetime import date
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    img=models.ImageField(upload_to="category")
    def __str__(self):
        return self.name

class Product(models.Model):
    categor=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    img=models.ImageField(upload_to="product")
    discription=models.TextField()
    quantity=models.IntegerField()
    price=models.IntegerField()
    def __str__(self):
        return self.name


class Register(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact=models.IntegerField()
    img=models.ImageField(upload_to="images")
    password=models.CharField(max_length=15)



class feedback(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact=models.IntegerField()
    message=models.TextField()

class Cartmodel(models.Model):
    orderid=models.CharField(max_length=200)
    userid=models.CharField(max_length=200)
    productid=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    totalprice=models.CharField(max_length=200)

class Ordermodel(models.Model):
    userid=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    useremail=models.EmailField()
    usercontact=models.CharField(max_length=200)
    address=models.TextField()
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.CharField(max_length=200)
    orderamount=models.CharField(max_length=200)
    paymentvia=models.CharField(max_length=200)
    paymentmethod=models.CharField(max_length=200)
    transactionid=models.TextField()
    orderdatetime=models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self) -> str:
        orderid=self.pk
        return str(orderid)