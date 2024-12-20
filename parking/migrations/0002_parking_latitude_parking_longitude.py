# Generated by Django 5.1.3 on 2024-12-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0.0, help_text='Garis lintang lokasi parkir', max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parking',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0.0, help_text='Garis bujur lokasi parkir', max_digits=9),
            preserve_default=False,
        ),
    ]
