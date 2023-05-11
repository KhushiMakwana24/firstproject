from django.contrib import admin

# Register your models here.
from app1.models import *

admin.site.register(Category)

class registerdisp(admin.ModelAdmin):
    list_display=['name','email','contact']
admin.site.register(Register,registerdisp)

class feedbackdisp(admin.ModelAdmin):
    list_display=['name','email','contact']
admin.site.register(feedback,feedbackdisp)

admin.site.register(Product)
class cartdisp(admin.ModelAdmin):
    list_display=['orderid','userid','productid']
admin.site.register(Cartmodel,cartdisp)

admin.site.register(Ordermodel)
