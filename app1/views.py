from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import *
from django.db.models import Q
# Create your views here.
def data(request):
    return HttpResponse('<h1>this is my first page</h1>')

def data2(request):
    if 'user' in request.session:
        data=request.session['user']
        abc=Category.objects.all()
        return render(request,'index.html',{'data':data,'abc':abc})
    else:
        abc=Category.objects.all()
        return render(request,'index.html',{'abc':abc})


def login(request):
    if request.method=="POST":
        email1=request.POST['email']
        password1=request.POST['password']
        try:
            data=Register.objects.get(email=email1,password=password1)
            if data:
                request.session['user']=data.email
                request.session['userid']=data.pk
                return redirect('home')
            else:
                return render(request,'login.html')
        except:
            return render(request,'login.html',{"message":"invalid password"})
    return render(request,'login.html')
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('login')
    else:
        return redirect('login')

def register(request):
    if request.method=="POST" and request.FILES:
        model=Register()
        model.name=request.POST['name']
        model.email=request.POST['email']
        model.contact=request.POST['contact']
        model.password=request.POST['pass']
        model.img=request.FILES['img']
        data=Register.objects.filter(email=request.POST['email'])
        if len(data)==0:
            model.save()
            return redirect('login')
        else:
            return render(request,'register.html',{"message":"user alredy exisist"})
    return render(request,'register.html')


def Profile(request):
    if 'user' in request.session:
        data=request.session['user']
        a=Register.objects.get(email=request.session['user'])
        print("data123",a)
        if request.method=="POST":
            a.name=request.POST['name']
            a.contact=request.POST['contact']
            a.save()
            return redirect('Profile')
        return render(request,'profile.html',{'a':a,'data':data})
    else:
        return redirect('login')
    

def Feedback(request):
    if 'user' in request.session:
        data=request.session['user']
        if request.POST:
            model=feedback()
            model.name=request.POST['name']
            model.email=request.POST['email']
            model.contact=request.POST['contact']
            model.message=request.POST['message']
            model.save()
            return render(request,'feedback.html',{'data':data,"m":"feedback sent"})
        return render(request,'feedback.html',{'data':data})
    else:
        return redirect('login')
    
def allproduct(request):
    if 'user' in request.session:
        data=request.session['user']
        pr=Product.objects.all()
        return render(request,'product.html',{'data':data,'product':pr})
    else:
        return redirect('login')
    
def categorywiseproduct(request,id):
    if 'user' in request.session:
        data=request.session['user']
        pr=Product.objects.filter(categor=id)
        return render(request,'product.html',{'data':data,'product':pr})
    else:
        return redirect('login')


def changepass(request):
    if 'user' in request.session:
        data=request.session['user']
        a=Register.objects.get(email=request.session['user'])
        if request.method=="POST":
            if a.password==request.POST['oldpass']:
                a.password=request.POST['newpass']
                a.save()
                return render(request,'changepass.html',{'a':a,'data':data,'m':"password changed"})
            else:
                return render(request,'changepass.html',{'a':a,'data':data,'m':"invalid old password"})
        return render(request,'changepass.html',{'a':a,'data':data})
    else:
        return redirect('login')
    
def productdetails(request,id):
    if 'user' in request.session:
        data=request.session['user']
        pr=Product.objects.get(id=id)
        if  request.POST:
            model=Cartmodel()
            model.orderid="0"
            model.userid=request.session['userid']
            model.productid=pr.pk
            model.quantity=request.POST['quantity']
            model.price=pr.price
            model.totalprice=int(pr.price)*int(model.quantity)
            a=Cartmodel.objects.filter(productid=pr.pk) & Cartmodel.objects.filter(orderid="0") & Cartmodel.objects.filter(userid=request.session['userid'])
            if len(a)==0:
                if pr.quantity>=int(model.quantity):
                    model.save()
                    pr.quantity=pr.quantity-int(model.quantity)
                    pr.save()
                    return render(request,'productdetails.html',{'data':data,'product':pr,"m":"Product Added"})
                else:
                    return render(request,'productdetails.html',{'data':data,'product':pr,"m":"Quantity not available"})
            else:
                return render(request,'productdetails.html',{'data':data,'product':pr,"m":"alredy  available"})
        return render(request,'productdetails.html',{'data':data,'product':pr})
    else:
        return redirect('login')
    

    
def cartview(request):
    if 'user' in request.session:
        data=request.session['user']
        cartdata=Cartmodel.objects.filter(userid=request.session['userid']) & Cartmodel.objects.filter(orderid="0")
        cartlist=[]
        totalamt=0
        for i in cartdata:
            totalamt=totalamt+int(i.totalprice)
            cartid=i.pk
            productdata=Product.objects.get(id=i.productid)
            prodctname=productdata.name
            productprice=i.price
            quantity=i.quantity
            totalprice=i.totalprice
            productimg=productdata.img
            prodict={'id':cartid,'prodctname':prodctname,'quantity':quantity,'productprice':productprice,'totalprice':totalprice,'productimg':productimg}
            cartlist.append(prodict)

        return render(request,'cart.html',{'data':data,'cartlist':cartlist,'noitem':len(cartlist),'finaltotalamt':totalamt})
    else:
        return redirect('login')
    
def remove_cartitem(request,id):
    if 'user' in request.session:
        a=Cartmodel.objects.get(id=id)
        data=Product.objects.get(id=a.productid)
        data.quantity=data.quantity+int(a.quantity)
        data.save()
        a.delete()
        return redirect('cartview1')    
    else:
        return redirect('login')
    

def removeall_cartitem(request):
    if 'user' in request.session:
        a=Cartmodel.objects.all()
        for i in a:
            data=Product.objects.get(id=i.productid)
            data.quantity=data.quantity+int(i.quantity)
            data.save()
        a.delete()
        return redirect('cartview1')    
    else:
        return redirect('login')
    
def searchview(request):
    word=request.GET.get('search')
    wordset=word.split(" ")
    for i in wordset:
        b=Product.objects.filter(Q(categor__name__icontains=i)|Q(name__icontains=i)|Q(price__icontains=i)).distinct()
    return render(request,'product.html',{'product':b})


def shiping(request):
    if 'user' in request.session:
        data=Register.objects.get(email=request.session['user'])
        cartdata=Cartmodel.objects.filter(userid=request.session['userid']) & Cartmodel.objects.filter(orderid="0")
        totalamt=0
        for i in cartdata:
            totalamt+=int(i.totalprice)
        if request.POST:
            model=Ordermodel()
            model.userid=request.session['userid']
            model.username=request.POST['userName']
            model.useremail=request.POST['userEmail']
            model.usercontact=request.POST['userContact']
            model.address=request.POST['address']
            model.city=request.POST['city']
            model.state=request.POST['state']
            model.pincode=request.POST['pincode']
            model.orderamount=request.POST['orderAmount']
            model.paymentvia=request.POST['paymentVia']
            if model.paymentvia=='Cash':
                model.paymentmethod=""
                model.transactionid=""
                model.save()
                orderid=Ordermodel.objects.latest('id')
                for i in cartdata:
                    cartproduct=Cartmodel.objects.get(id=i.pk)
                    cartproduct.orderid=str(orderid)
                    cartproduct.save()
                return  redirect('orderSuccessView')
            else:
                request.session['shippingUserId'] = request.session['userid']
                request.session['shippingName'] = request.POST['userName']
                request.session['shippingEmail'] = request.POST['userEmail']
                request.session['shippingContact'] = request.POST['userContact']
                request.session['shippingAddress'] = request.POST['address']
                request.session['shippingCity'] = request.POST['city']
                request.session['shippingState'] = request.POST['state']
                request.session['shippingPincode'] = request.POST['pincode']
                request.session['shippingOrderAmount'] = str(totalamt)
                request.session['shippingPaymentVia'] = "Online"
                request.session['shippingPaymentMethod'] = "Razorpay"
                request.session['shippingTransactionId'] = ""
                return redirect('razorpayView')
        return render(request,'shiping.html',{'data1':data,'totalamt':totalamt})   
    else:
        return redirect('login')
    
def orderSuccessView(request):
    if 'user' in request.session:
        data=request.session['user']
        return render(request,'order_sucess.html',{'data':data})
    else:
        return redirect('login')
    
def myorder(request):
    if 'user' in request.session:
        data=request.session['user']
        orderdata=Ordermodel.objects.filter(userid=request.session['userid']).order_by('-id')
        if request.POST:
            request.session['orderid']=request.POST['orderId']
            return redirect('myorderdetails')
        return render(request,'myorder.html',{'data':data,'orderdata':orderdata})
    else:
        return redirect('login')
    
def myorderdetails(request):
    if 'user' in request.session:
        data=request.session['user']
        orderid=request.session['orderid']
        del request.session['orderid']
        orderdata=Ordermodel.objects.get(id=orderid)
        address=orderdata.address+" "+orderdata.city+" "+orderdata.state+" "+orderdata.pincode
        orderdict={
            'name':orderdata.username,
            'contact':orderdata.usercontact,
            'address':address,
            'orderamt':orderdata.orderamount,
            'paymentvia':orderdata.paymentvia,
            'paymentmethod':orderdata.paymentmethod,
            "transactionid":orderdata.transactionid
        }
        cartdata=Cartmodel.objects.filter(orderid=orderid)
        cartlist=[]
        for i in cartdata:
            
            productdata=Product.objects.get(id=i.productid)
            cartdict={
                'productname':productdata.name,
                'productimg':productdata.img.url,
                'qty':i.quantity,
                'price':i.price,
                'totalprice':i.totalprice
            }
            cartlist.append(cartdict)
        return render(request,'orderdetails.html',{'data':data,'orderdict':orderdict,'cartlist':cartlist})
    else:
        return redirect('login')

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


RAZOR_KEY_ID = 'rzp_test_8iwTTjUECLclBG'
RAZOR_KEY_SECRET = '0q8iXqBL1vonQGVQn4hK1tYg'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['shippingOrderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['shippingOrderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)
            #Order Save Code
            orderModel = Ordermodel()
            orderModel.userid = request.session['shippingUserId']
            orderModel.username = request.session['shippingName']
            orderModel.useremail = request.session['shippingEmail']
            orderModel.usercontact = request.session['shippingContact']
            orderModel.address = request.session['shippingAddress']
            orderModel.city = request.session['shippingCity']
            orderModel.state = request.session['shippingState']
            orderModel.pincode = request.session['shippingPincode']
            orderModel.orderamount = request.session['shippingOrderAmount']
            orderModel.paymentvia = request.session['shippingPaymentVia']
            orderModel.paymentmethod = request.session['shippingPaymentMethod']
            orderModel.transactionid = payment_id
            orderModel.save()
            orderId = Ordermodel.objects.latest('id')
            cartdata=Cartmodel.objects.filter(userid=request.session['userid']) & Cartmodel.objects.filter(orderid="0")
            for i in cartdata:
                cartData = Cartmodel.objects.get(id=i.pk)
                cartData.orderid = str(orderId)
                cartData.save()
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
