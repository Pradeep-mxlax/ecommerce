from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import *
from django.views import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import *
# Create your views here.

class HomeView(ListView):
    """ user home page class """

    model = Category
    template_name = "myapp/home_detail.html"
    context_object_name = 'categories'


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

    def post(slef,request):
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


class CartView(TemplateView):
    """ user cart  class """

    template_name = "myapp/cart.html"


class DetailView(TemplateView):
    """ user product detail class """

    template_name = "myapp/detail.html"

class ShopView(TemplateView):
    """ user product shop class """

    template_name = "myapp/shop.html"


class CheckoutView(TemplateView):
    """ user product checkout class """

    template_name = "myapp/checkout.html"

class ProfileView(View):
    """ user profile class """
    def get(self,request):
        user_detais = request.user
        return render(request, 'user/profile.html',{'user_detais':user_detais})

# 

