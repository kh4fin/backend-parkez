from django.urls import path
from . import views

urlpatterns = [
    path('parking/', views.parking_list_create, name='parking-list-create'),
    path('parking/<int:pk>/', views.parking_detail, name='parking-detail'),

    path('paket/', views.paket_list_create, name='paket-list-create'),
    path('paket/<int:pk>/', views.paket_detail, name='paket-detail'),

    path('paket/beli/', views.beli_paket, name='beli-paket'),

    path('midtrans/notification/', views.midtrans_notification, name='midtrans-notification'),

    path('parkir/checkin/', views.checkin_parkir, name='checkin-parkir'),
]
