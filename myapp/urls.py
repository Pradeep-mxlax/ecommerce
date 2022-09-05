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
    path('detail/<int:pid>',views.DetailView.as_view(),name='detail'),
    path('shop/<int:sid>',views.ShopView.as_view(),name='shop'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('cartitem/',views.CartItemView.as_view(),name='cartitem'),
    path('cartitemdelete/<int:id>',views.CartItemDeleteView.as_view(),name='cartitemdelete'),
    path('address/',views.AddressView.as_view(),name='address'),
    path('editaddress/',views.editAddress,name='editaddress'),
    path('delete_address/',views.DeleteAddressView.as_view(),name='delete_address'),
    path('search/',views.SearchView.as_view(),name='search'),   
    path('order_place/',views.orderPlaceView.as_view(),name='order_place'),
    path('orders/',views.OrderView.as_view(),name='orders'),
    path('orders_details/',views.OrderDetailsView.as_view(),name='orders_details'),
    path('rating/',views.RatingView.as_view(),name='rating'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
