from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Paket(models.Model):
    nama_paket = models.CharField(max_length=100)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    diskon = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    durasi_hari = models.IntegerField(help_text="Durasi paket dalam hari")
    benefits = models.TextField(help_text="Daftar manfaat, pisahkan dengan koma", blank=True)
    tipe_paket = models.CharField(max_length=100)
    kendaraan = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_paket

class Parking(models.Model):
    nama_tempat = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=255)
    koordinat = models.CharField(max_length=20, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Garis lintang lokasi parkir")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Garis bujur lokasi parkir")
    tipe_kendaraan = models.CharField(max_length=20, choices=(('mobil', 'Mobil'), ('motor', 'Motor')))
    kapasitas = models.IntegerField()
    terpakai = models.IntegerField(default=0)

    def __str__(self):
        return self.nama_tempat

class TransaksiPaket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paket = models.ForeignKey(Paket, on_delete=models.CASCADE)
    durasi_aktif = models.DateTimeField(help_text="Waktu berakhir masa aktif paket")
    status = models.CharField(max_length=20, choices=(('paid', 'Paid'), ('unpaid', 'Unpaid')), default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.paket.nama_paket} - {self.status}"

class CheckInParkir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    waktu_checkin = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.parking.nama_tempat}"
