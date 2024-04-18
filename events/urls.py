from django.urls import path
from .views import event_list, event_create, event_update, event_delete, event_register, unregister, registered_events

app_name = 'events'

urlpatterns = [
    path('', event_list, name='event_list'),
    path('add/', event_create, name='event_create'),  # URL for adding a new event
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('<int:pk>/register/', event_register, name='event_register'),
    path('<int:pk>/unregister/', unregister, name='unregister'),
    path('registered-events/', registered_events, name='registered_events'),
    
]