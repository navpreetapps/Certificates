# Generated by Django 4.2.3 on 2023-07-25 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cer_ser', '0003_certificate_owners_certificate_tokens_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificates',
            old_name='date_pos_right',
            new_name='date_pos_left',
        ),
        migrations.RenameField(
            model_name='certificates',
            old_name='signature_pos_right',
            new_name='signature_pos_left',
        ),
    ]
