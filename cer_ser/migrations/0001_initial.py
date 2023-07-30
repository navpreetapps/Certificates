# Generated by Django 4.2.3 on 2023-07-22 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('content_pos', models.CharField(max_length=255)),
                ('signature_pos', models.CharField(max_length=255)),
                ('date_pos', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('certificates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cer_ser.certificates')),
            ],
        ),
    ]
