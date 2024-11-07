from rest_framework import serializers
from .models import TransaksiPaket, Paket, Parking, CheckInParkir

class PaketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paket
        fields = ['id', 'nama_paket', 'deskripsi', 'harga', 'diskon', 'durasi_hari']

class TransaksiPaketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiPaket
        fields = ['id', 'user', 'paket', 'durasi_aktif', 'status', 'created_at']

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id', 'nama_tempat', 'lokasi', 'kode_lokasi', 'tipe_kendaraan', 'kapasitas', 'terpakai']

class CheckInParkirSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInParkir
        fields = ['id', 'user', 'parking', 'waktu_checkin']
