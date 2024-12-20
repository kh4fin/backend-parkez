# Generated by Django 5.1.3 on 2024-11-11 00:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_paket', models.CharField(max_length=100)),
                ('deskripsi', models.TextField()),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('diskon', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('durasi_hari', models.IntegerField(help_text='Durasi paket dalam hari')),
                ('benefits', models.TextField(blank=True, help_text='Daftar manfaat, pisahkan dengan koma')),
                ('tipe_paket', models.CharField(max_length=100)),
                ('kendaraan', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_tempat', models.CharField(max_length=100)),
                ('lokasi', models.CharField(max_length=255)),
                ('koordinat', models.CharField(max_length=20, unique=True)),
                ('tipe_kendaraan', models.CharField(choices=[('mobil', 'Mobil'), ('motor', 'Motor')], max_length=20)),
                ('kapasitas', models.IntegerField()),
                ('terpakai', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CheckInParkir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_checkin', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.parking')),
            ],
        ),
        migrations.CreateModel(
            name='TransaksiPaket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('durasi_aktif', models.DateTimeField(help_text='Waktu berakhir masa aktif paket')),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.paket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
