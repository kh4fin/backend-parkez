from django.urls import path
from . import views

urlpatterns = [
    # Parking URLs
    path('parking/', views.parking_list_create, name='parking-list-create'),
    path('parking/<int:pk>/', views.parking_detail, name='parking-detail'),

    # Paket URLs
    path('paket/', views.paket_list_create, name='paket-list-create'),
    path('paket/<int:pk>/', views.paket_detail, name='paket-detail'),

    # Beli Paket
    path('paket/beli/', views.beli_paket, name='beli-paket'),

    # Midtrans Notification
    path('midtrans/notification/', views.midtrans_notification, name='midtrans-notification'),

    # Check-in Parkir
    path('parkir/checkin/', views.checkin_parkir, name='checkin-parkir'),
]
