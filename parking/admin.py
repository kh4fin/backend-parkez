from django.contrib import admin
from .models import Paket, Parking, TransaksiPaket, CheckInParkir


admin.site.register(Paket)
admin.site.register(Parking)
admin.site.register(TransaksiPaket)
admin.site.register(CheckInParkir)