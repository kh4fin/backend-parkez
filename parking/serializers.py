from rest_framework import serializers
from .models import TransaksiPaket, Paket, Parking, CheckInParkir


class PaketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paket
        fields = [
            'id',
            'nama_paket',
            'deskripsi',
            'harga',
            'diskon',
            'durasi_hari',
            'benefits',
            'tipe_paket',
            'kendaraan'
        ]
        read_only_fields = ['id']


class TransaksiPaketSerializer(serializers.ModelSerializer):
    paket = PaketSerializer(read_only=True)  
    class Meta:
        model = TransaksiPaket
        fields = [
            'id',
            'user',
            'paket',
            'durasi_aktif',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'durasi_aktif', 'status', 'created_at']


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = [
            'id',
            'nama_tempat',
            'lokasi',
            'koordinat',
            'tipe_kendaraan',
            'kapasitas',
            'terpakai'
        ]
        read_only_fields = ['id']


class CheckInParkirSerializer(serializers.ModelSerializer):
    parking = ParkingSerializer(read_only=True)  
    class Meta:
        model = CheckInParkir
        fields = [
            'id',
            'user',
            'parking',
            'waktu_checkin'
        ]
        read_only_fields = ['id', 'waktu_checkin']

