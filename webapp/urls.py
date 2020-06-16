from django.urls import path
from .views import HomeView, help, about

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('help/', help, name='help'),
    path('about/', about, name='about'),
]