from django.urls import path, include
from .views import register, login, logoutaccount, reports

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logoutaccount, name='logout'),
    path('reports', reports, name='reports')
  
]