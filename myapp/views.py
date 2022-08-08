from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import *
from django.views import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.utils.translation import gettext 
# Create your views here.
class HomeView(TemplateView):
    template_name = "myapp/home.html"

class RegistrationView(View):
    def get(self,request):
        form = NewRegisterForm()
        return render(request, 'user/register.html',{'form':form})

    def post(self,request):
        form = NewRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'user/register.html',{'form':form})

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        print(request.user)
        return render(request, 'user/login.html',{'form':form})

    def post(slef,request):
        form = LoginForm(data=request.POST)
        data=request.POST
        print(data)
        # print(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,password)
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('user not found')

        else:
            return render(request, 'user/login.html',{'form':form})

class loguotView(View):
    def get(self,request):
        logout(request)
        return redirect('/')