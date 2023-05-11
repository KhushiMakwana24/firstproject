from django.urls import path
from app1.views import *
urlpatterns = [
    path('home/',data,name="home1"),
    path('',data2,name='home'),
    path('login/',login ,name="login"),
    path('logout/',logout ,name="logout"),
    path('register/',register,name="register"),
    path('Profile/',Profile,name="Profile"),
    path('feedback/',Feedback,name="feedback"),
    path('allproduct/',allproduct,name="allproduct"),
    path('categorywiseproduct/<int:id>',categorywiseproduct,name="categorywiseproduct"),
    path('changepass',changepass,name="changepass"),
    path('productdetails/<int:id>',productdetails,name="productdetails1"),
    path('cartview',cartview,name="cartview1"),
    path('remove_cartitem/<int:id>',remove_cartitem,name="remove_cartitem1"),
    path('removeall_cartitem/',removeall_cartitem,name="removeall_cartitem1"),
    path('searchview/',searchview,name="search"),
    path('shiping/',shiping,name="shiping1"),
    path('orderSuccessView/',orderSuccessView,name='orderSuccessView'),
    path('my-order/',myorder,name='myorder'),
    path('my-orderdetails/',myorderdetails,name='myorderdetails'),
    path('razorpayView/',razorpayView,name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
]