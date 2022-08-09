from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('register/',views.RegistrationView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('loguot/',views.loguotView.as_view(),name='loguot'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('detail/',views.DetailView.as_view(),name='detail'),
    path('shop/',views.ShopView.as_view(),name='shop'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)