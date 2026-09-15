from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('park/', views.park_vehicle, name='park_vehicle'),
    path('exit/', views.exit_vehicle, name='exit_vehicle'),
    path('get_slots/', views.get_slots, name='get_slots'),
    path('predict/', views.parking_prediction, name='predict'),  # ✅ ADD HERE
]