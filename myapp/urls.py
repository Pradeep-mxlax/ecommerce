from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('register/',views.RegistrationView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('loguot/',views.loguotView.as_view(),name='loguot'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)