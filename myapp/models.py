from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class User_More_Detail(models.Model):
    GENDER = [    
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='normal_user')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    gender = models.CharField(max_length=10,choices=GENDER)
    date_of_birth = models.DateField()
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Address(models.Model):
    """User address which one store user addres"""

    # STATE = [
    #     ('MP','Madhya Pradesh'),
    #     ('GU','Gujrat')
    # ]
    # COUNTRY = [
    #     ('END','England'),sss
    #     ('IND','India')
    # ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='address_user')
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    address1 = models.TextField()
    pin_code = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50,default='')
    country = models.CharField(max_length=50,default='')
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitute = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.name

class Category(models.Model):
    """ Product category model """

    category_name = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    """ Product Subcategty model  """

    category = models.ManyToManyField(Category,related_name='sub_cat')
    sub_cat_name = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_cat_name

class Product(models.Model):
    """  Product model """

    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='prd_cat')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='prd_subcat')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    product_sku = models.CharField(max_length=100,unique=True)
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    total_stock_unit = models.PositiveIntegerField(default=0)
    sold_stock_unit = models.PositiveIntegerField(default=0) 
    available_on = models.DateTimeField(auto_now_add=True,editable=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    """ store all media files of product  """
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='media_prd')
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    

class Cart(models.Model):
    """product cart models """

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart_user')
    quantity = models.IntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    


class CartItem(models.Model):
    """ add  product into cart item """

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='prd_cartitem')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_cartitem')
    quantity = models.IntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)
    payed = models.BooleanField(default=False) 
    add_date = models.DateTimeField(auto_now_add=True)

    @property
    def new_total_price(self):
        return self.quantity * self.product_id.price


class Order(models.Model):
    """ product order model"""
    PAYMENT = [
        ('none','none'),
        ('cash','cash'),
        ('debit','debit cart'),
        ('paytm','paytm'),
        ('bank','Bank Transfer'),
    ]

    ORDER_STATUS = [    
        ('Success','Success'),
        ('On the way','On the way'),
        ('Refund','Refund'),
        ('Failed','Failed')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='admin_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='prd_order',null=True,blank=True) 
    carts = models.ManyToManyField(CartItem,null=True,blank=True) 
    quantity = models.IntegerField(default=0)   
    price = models.PositiveIntegerField(default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='order_address')
    order_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=ORDER_STATUS)
    payment = models.CharField(max_length=10,choices=PAYMENT,default='none')



    # class OrderDetails(models.Model):
    #     orders = models.models.ManyToManyField(Order)
    