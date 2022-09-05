from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.generic import *
from django.views import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
# from django.db.models.query import RawQuerySet
# from django.db import connection
class HomeView(View):
    """ user home page class """
    def get(self,request):
        categories = Category.objects.all()
        product_data = Product.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            cartitem = CartItem.objects.filter(cart=cart,payed='False')
            if not cart:
                Cart.objects.create(user=request.user)
        
            context = {
                    'categories' : categories,
                    'product_data' : product_data,
                    'cartitem' : cartitem,

            }
            return render(request, "myapp/home_detail.html",context)
        else:

            context = {
                    'categories' : categories,
                    'product_data' : product_data,
            }
            return render(request, "myapp/home_detail.html",context)

class RegistrationView(View):
    """ user register class """

    def get(self,request):
        form = NewRegisterForm()
        return render(request, 'user/register.html',{'form':form})

    def post(self,request):
        form = NewRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'user/register.html',{'form':form})


class LoginView(View):
    """ user login class """

    def get(self,request):
        form = LoginForm()
        return render(request, 'user/login.html',{'form':form})

    def post(self,request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('user not found')

        else:
            return render(request, 'user/login.html',{'form':form})


class loguotView(View):
    """ user logout class """

    def get(self,request):
        logout(request)
        return redirect('/')


class ProfileView(View):
    """ user profile class """
    def get(self,request):
        if request.user.is_authenticated:
            address = Address.objects.filter(user=request.user).order_by('-id')
            user = request.user   
            user_data = User_More_Detail.objects.filter(user=request.user).first()
            context = {
                        'user':user,
                        'address':address,
                        'user_data' : user_data
                        }
            return render(request, 'user/profile.html',context)
        return redirect('login')
    def post(self,request):
        user_data = User_More_Detail.objects.filter(user=request.user).first()
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        image = request.FILES.get('image')
        gender = request.POST['gender']
        birth = request.POST['dob']
        if image is None:
            messages.info(request, 'please add image ')
            return redirect('/profile/')
        if user_data:
            user_data.first_name=first_name
            user_data.last_name=last_name
            user_data.image=image
            user_data.gender=gender
            user_data.date_of_birth=birth
            user_data.save()
        else:
            User_More_Detail(user=request.user,first_name=first_name,last_name=last_name,image=image,gender=gender,date_of_birth=birth).save()
        return redirect('profile')


class CartView(View):
    """ user cart  class """
    def get(self,request,*args,**kwargs):

        if request.user.is_authenticated:
            carts = Cart.objects.get(user=request.user)
            cartitem  = carts.cart_cartitem.filter(payed='False')
            new_total = 0
            for data in cartitem:
                new_total+=data.total_price
            carts.total_price = new_total
            carts.save()
            context = {
                    'cartitem':cartitem,
                    'cart':carts
            }
            return render(request, 'myapp/cart.html',context)
        else:
            return redirect('login')
    def post(self,request,*args,**kwargs):
        carts = Cart.objects.get(user=request.user)
        quntity = request.POST.get('quantity')
        button_type = request.POST.get('type')
        product_id = request.POST.get('product')
        cartitem = CartItem.objects.get(product_id=product_id,cart=carts,payed='False')
        product_price = Product.objects.get(id=product_id)
        if button_type == 'plus':
            if int(quntity) < product_price.total_stock_unit:
                if int(quntity) < 5:
                    cartitem.quantity+=1
                    cartitem.total_price = cartitem.new_total_price
                    cartitem.save()
                messages.info(request, "We're sorry! Only 5 units allowed in each order")
                return redirect('cart')
            messages.info(request, "We're sorry! No more availlabe stock of this product  ")
            return redirect('cart')
        elif button_type == 'minus':
            if cartitem.quantity > 1:
                cartitem.quantity-=1
                cartitem.total_price =  cartitem.new_total_price
                cartitem.save()  
 
        return redirect('cart')


class CartItemView(View):

    def get(self,request,*args, **kwargs):
        return redirect('cart')

    def post(self,request,*args, **kwargs):
        if  request.user.is_authenticated:
            prduct_id = request.POST.get('prduct_id')
            product = Product.objects.get(id=prduct_id)
            carts = Cart.objects.get(user=request.user)
            available_product =carts.cart_cartitem.filter(product_id=prduct_id,payed='False')
            if not available_product :
                CartItem.objects.create(product_id=product,cart=carts,total_price=product.price)

                return redirect('cart')
            else:
                return redirect('cart') 
        else:
            return redirect('login')
     

class CartItemDeleteView(View):

    def get(self,request,*args, **kwargs):
        cartitem = CartItem.objects.get(id=kwargs['id'])
        carts = Cart.objects.get(user=request.user)
        total = carts.total_price
        product_price = cartitem.total_price
        new_price = total - product_price
        carts.total_price = new_price
        carts.save()
        cartitem.delete()

        return redirect('cart')


class DetailView(View):
    """ user product detail class """

    def get(self,request,*args,**kwargs):
        categories = Category.objects.all()
        product_data = Product.objects.get(id=kwargs['pid'])
        # p = Product.objects.filter(category=product_data.category).exclude(id=kwargs['pid'])
        # print('prolfjh',p)
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cartitem = CartItem.objects.filter(cart=cart,payed='False')
            context = {
                    'categories' : categories,
                    'product_data' : product_data,
                    'cartitem' : cartitem,
            }
            return render(request, "myapp/detail.html",context)
        else:
            context = {
                    'categories' : categories,
                    'product_data' : product_data,
            }
        return render(request, "myapp/detail.html",context)


class ShopView(View):
    """ user product shop class """   

    def get(self,request,*args,**kwargs):

        categories = Category.objects.all()
        sub_data = SubCategory.objects.get(id=kwargs['sid'])
        product_data= Product.objects.filter(sub_category=sub_data)
        # import pdb;pdb.set_trace()
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cartitem = CartItem.objects.filter(cart=cart,payed='False')
            context = {
                    'categories' : categories,
                    'product_data' : product_data,
                    'cartitem' : cartitem,
            }
            return render(request, "myapp/shop.html",context)
        else:
            context = {
                    'categories' : categories,
                    'product_data' : product_data,
            }
            return render(request, "myapp/shop.html",context)



class CheckoutView(View):
    """ user product checkout class """

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            product_id = request.GET.get('pr_id')
            address = Address.objects.filter(user=request.user)
            carts = Cart.objects.get(user=request.user)
            if product_id:
                product_data = Product.objects.get(id=product_id)
                context = {
                            'prd':product_data,
                            'address' : address
                }
                return render(request, "myapp/checkout.html",context)
            else:
                cartitem = CartItem.objects.filter(cart=cart,payed='False')
                # import pdb;pdb.set_trace()
                context = {
                            'cart':cart,
                            'cartitem':cartitem,
                            'address' : address
                }
                return render(request, "myapp/checkout.html",context)
        else:
            return redirect('login')
        # return render(request, "myapp/checkout.html")

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            product_id = request.GET.get('pr_id')
            address = Address.objects.filter(user=request.user).order_by('-id')
            carts = Cart.objects.get(user=request.user)
            if product_id:
                available_product =carts.cart_cartitem.filter(product_id=product_id)
                product_data = Product.objects.get(id=product_id)
                if not available_product :
                    CartItem.objects.create(product_id=product_data,cart=carts,total_price=product_data.price)
                context = {
                            'prd':product_data,
                            'address' : address
                }
                return render(request, "myapp/checkout.html",context)
            else:
                
                cartitem = CartItem.objects.filter(cart=carts,payed='False')
                context = {
                            'cart':carts,
                            'cartitem':cartitem,
                            'address' : address
                }
                return render(request, "myapp/checkout.html",context)
        else:
            return redirect('login')


class ContactView(TemplateView):
    """ user product checkout class """

    template_name = "myapp/contact.html"


class AddressView(View):
    """ user product checkout class """

    def post(self,request,*args, **kwargs):
        # import pdb;pdb.set_trace()
        pid = request.GET['pr_id']
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        Address.objects.create(user=request.user,name=name,phone_number=number,address1=address,pin_code=pincode,city=city,state=state,country=country)
        if pid == 'yes':
            user_data = request.user   
            return render(request, 'user/profile.html',{'user_data':user_data}) 
        else:
            return redirect(f'/checkout/?pid={pid}')

def editAddress(request):
    if request.method == "POST":
        pid = request.GET.get('pr_id')
        address_id = request.POST['address_id']
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        Address.objects.filter(id=address_id).update(user=request.user,name=name,phone_number=number,address1=address,pin_code=pincode,city=city,state=state,country=country)
        if pid == 'yes':
            return redirect('profile')
        else:
            return redirect(f'/checkout/?pid={pid}')
       

class SearchView(View):
    def get(self,request,*args, **kwargs):
        data = request.GET.get('search')
        product_list = set()
        categories = Category.objects.all()
        product_data = Product.objects.filter(title__icontains=data)
        category_data = Category.objects.filter(category_name__icontains=data).filter(category_name__istartswith=data)

        subcategory_data = SubCategory.objects.filter(sub_cat_name__icontains=data)
        
        for prd in product_data:
            product_list.add(prd)
            print('product',prd)
        for sub in subcategory_data:
            for data in sub.prd_subcat.all():
                product_list.add(data)
            print('sub',sub)
        for cat in category_data:
            for data in cat.prd_cat.all():
                product_list.add(data)
            print('caat',cat) 
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cartitem = CartItem.objects.filter(cart=cart,payed='False')
            context ={
                    'product_list':list(product_list),
                    'categories' : categories,
                    'cartitem' : cartitem,
                    }
            return render(request, "myapp/search.html",context)
        else:
            context ={
                    'product_list':list(product_list),
                    'categories' : categories,
                    }
            return render(request, "myapp/search.html",context)


class DeleteAddressView(View):
    def get(self,request,*args, **kwargs):
        address_id = request.GET.get('address_id')
        Address.objects.filter(id=address_id).delete()
        return redirect('profile')


class orderPlaceView(View):
   def post(self,request,*args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quntitys_id')
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment')

        address = Address.objects.get(id=address_id)
        cart = Cart.objects.get(user=request.user)
        orders = Order(user=request.user,address=address,status='Success',payment=payment_method)
        orders.save()
        if product_id:
            product = Product.objects.get(id=product_id)
            cartitem = cart.cart_cartitem.get(product_id=product,payed='False')
            orders.carts.add(cartitem)
            cartitem.product_id.total_stock_unit-=int(quantity)
            cartitem.product_id.sold_stock_unit+=int(quantity)
            cartitem.product_id.save()
            cartitem.payed='True'
            cartitem.save()
        else:
            for data in cart.cart_cartitem.filter(payed='False'):
                orders.carts.add(data) 
                data.product_id.total_stock_unit-=data.quantity
                data.product_id.sold_stock_unit += data.quantity
                data.payed='True'
                data.save()
        return redirect('/')

class OrderView(View):
    def get(self,request,*args, **kwargs):
        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cartitem = CartItem.objects.filter(cart=cart,payed="False")
            order_item = Order.objects.filter(user=request.user).order_by('-id')
            context = {
                'categories':categories,
                'cartitem':cartitem,
                'order_items' : order_item
            }
            return render(request, 'myapp/order.html',context)
        else:
            return redirect('login')
        
class OrderDetailsView(View):
    def get(self,request,*args, **kwargs):
        order_id = request.GET.get('order_id')
        categories = Category.objects.all()
        order_item = Order.objects.filter(id=order_id)

        print(order_id)
        context = {
                    'categories' : categories,
                    'order_items' : order_item,
            }
        return render(request, 'myapp/order_details.html',context)

class OfferView(View):
    def get(self,request,*args, **kwargs):
        offers = Offer.objects.all()
        categories = Category.objects.all()
        context = {
                'offers':offers,
                'categories':categories
        }
        return render(request, 'myapp/offer.html',context)