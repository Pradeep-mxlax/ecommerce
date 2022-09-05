from django.contrib import admin
from myapp.models import *
# Register your models here.
admin.site.register(User_More_Detail)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name','city','phone_number','address1','state',]  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','description','create_date','update_date']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['sub_cat_name','description','create_date','update_date']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category','sub_category','name','price','product_sku','total_stock_unit','sold_stock_unit']

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
        list_display = ['product','image','description']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','quantity','total_price']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product_id','quantity','total_price','payed']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','order_date']


@admin.register(ProductRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user','product','rating']