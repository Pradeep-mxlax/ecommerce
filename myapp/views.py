from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import *
from django.views import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.views.generic.edit import DeleteView
# Create your views here.

class HomeView(View):
    """ user home page class """
# if request.user.is_authanticate():
    def get(self,request):
        if not request.user:
            Cart.objects.create(user=request.user)
        categories = Category.objects.all()
        product_data = Product.objects.all()
        context = {
                'categories' : categories,
                'product_data' : product_data
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
        print(request.user)
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

        user_data = request.user   
        return render(request, 'user/profile.html',{'user_data':user_data})
    
    def post(self,request):
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        img = request.FILES['image']
        gender = request.POST['gender']
        birth = request.POST['dob']
        User_More_Detail(user=request.user,first_name=first_name,last_name=last_name,image=img,gender=gender,date_of_birth=birth).save()
        # print(first_name,lastt_name,gender,birth,img)
        return redirect('profile')


class CartView(View):
    """ user cart  class """
    def get(self,request,*args,**kwargs):

        if request.user.is_authenticated:
            carts = Cart.objects.get(user=request.user)
            cartitem  = carts.cart_cartitem.all()
            return render(request, 'myapp/cart.html',{'cartitem':cartitem})
        else:
            return redirect('login')

class CartItemView(View):

    def get(self,request,*args, **kwargs):
        return redirect('cart')

    def post(self,request,*args, **kwargs):
        prduct_id = request.POST.get('prduct_id')
        product = Product.objects.get(id=prduct_id)
        carts = Cart.objects.get(user=request.user)
        CartItem.objects.create(product_id=product,cart=carts)
        # import pdb;pdb.set_trace()
        return redirect('cart')

class CartItemDeleteView(View):
    def get(self,request,*args, **kwargs):
        cartitem = CartItem.objects.get(id=kwargs['id'])
        cartitem.delete()
        return redirect('cart')
    # template_name = "myapp/cart.html"


class DetailView(View):
    """ user product detail class """
    def get(self,request,*args,**kwargs):

        categories = Category.objects.all()
        product_data = Product.objects.get(id=kwargs['pid'])
        print(product_data)
        context = {
                'categories' : categories,
                'product_data' : product_data
        }
        return render(request, "myapp/detail.html",context)

class ShopView(View):
    """ user product shop class """   
    def get(self,request,*args,**kwargs):

        categories = Category.objects.all()
        sub_data = SubCategory.objects.get(id=kwargs['sid'])
        product_data= Product.objects.filter(sub_category=sub_data)
        context = {
                'categories' : categories,
                'product_data' : product_data
        }
        return render(request, "myapp/shop.html",context)

class CheckoutView(TemplateView):
    """ user product checkout class """

    template_name = "myapp/checkout.html"

class ContactView(TemplateView):
    """ user product checkout class """

    template_name = "myapp/contact.html"