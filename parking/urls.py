from django.urls import path
from . import views

urlpatterns = [
    # Endpoint untuk daftar parkir
    path('parking/', views.parking_list_create, name='parking-list-create'),
    
    # Endpoint untuk detail parkir (PUT, DELETE, GET)
    path('parking/<int:pk>/', views.parking_detail, name='parking-detail'),

    # Endpoint untuk daftar paket
    path('paket/', views.paket_list_create, name='paket-list-create'),

    # Endpoint untuk detail paket (PUT, DELETE, GET)
    path('paket/<int:pk>/', views.paket_detail, name='paket-detail'),

    # Endpoint untuk membeli paket
    path('beli-paket/', views.beli_paket, name='beli-paket'),

    # Endpoint untuk notifikasi Midtrans
    path('midtrans-notification/<int:transaksi_id>/', views.midtrans_notification, name='midtrans-notification'),

    #Endpoind untuk list_paket_user
    path('list-paket-user/', views.list_paket_user, name='list_paket_user'),

    #Endpoind untuk generate qrcode
    path('generate-qrcode/<int:transaksi_id>/', views.generate_qrcode, name='generate_qrcode'),

    #Endpoind untuk verify qrcode
    path('verify-qrcode/<int:transaksi_id>/', views.verify_qrcode, name='verify_qrcode'),

    # Endpoint untuk check-in parkir
    path('checkin-parkir/<int:transaksi_id>/', views.checkin_parkir, name='checkin-parkir'),

    # Endpoint untuk riwayat transaksi paket
    path('transaksi-paket/', views.list_transaksi_paket, name='list-transaksi-paket'),

    # Endpoint untuk riwayat transaksi paket by user
    path('transaksi-paket-user/', views.list_transaksi_paket_by_User, name='list_transaksi_paket_by_User'),

    # Endpoint untuk riwayat check-in parkir
    path('checkin-parkir-history/', views.list_checkin_parkir, name='list-checkin-parkir'),
]
