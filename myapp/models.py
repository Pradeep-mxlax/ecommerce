from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

# class User(models.Model):
#     GENDER = [    
#         ('M','Male'),
#         ('F','Female'),
#     ]
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=100)
    
#     password = models.CharFiePld(max_length=20)
#     gender = models.CharField(max_length=2,choices=GENDER)
#     is_active = models.BooleanField(default=False)
#     date_join = models.DateTimeField(auto_now=True) 
    
#     def __str__(self):
        # return self.name


class Address(models.Model):
    """User address which one store user addres"""

    STATE = [
        ('MP','Madhya Pradesh'),
        ('GU','Gujrat')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    address1 = models.TextField(help_text='Enter Local address')
    address2 = models.TextField(help_text='Enter Permanent address',null=True,blank=True)
    address3 = models.TextField(help_text='Enter office address',null=True,blank=True)
    pin_code = models.PositiveIntegerField()
    state = models.CharField(max_length=5,choices=STATE)
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

    category = models.ManyToManyField(Category)
    sub_cat_name = models.CharField(max_length=255)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_cat_name

class Product(models.Model):
    """  Product model """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    product_sku = models.CharField(max_length=100)
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    # total_stock_unit = models.PositiveIntegerField()
    # sold_stock_unit = models.PositiveIntegerField() 
    available_on = models.DateTimeField(auto_now_add=True,editable=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Media(models.Model):
    """ store all media files of product  """
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    

# class ProductDetails(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    """product cart models """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.str(id)


class CartItem(models.Model):
    """ add  product into cart item """

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    payed = models.BooleanField(default=False) 
    add_date = models.DateTimeField(auto_now_add=True)

    # @property
    # def total_price(self):
    #     return self.quantity + self.product_id.price
    def __str__(self):
        return self.id


class Order(models.Model):
    """ product order model"""

    ORDER_STATUS = [    
        ('S','success'),
        ('W','On the way'),
        ('P','Pending'),
        ('F','Failed')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=ORDER_STATUS)

    def __str__(self):
        return self.id


# class OrderDetails(models.Model):
#     ordel = models.ForeignKey(to, on_delete=models.CASCADE)
#     product = 