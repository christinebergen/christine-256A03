from django.urls import path, include
from .views import register, login, logoutaccount, reports, user_list, admin_events_list

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logoutaccount, name='logout'),
    path('reports', reports, name='reports'),
    path('user_list', user_list, name='user_list'),
    path('admin_events_list', admin_events_list, name='admin_events_list')
]