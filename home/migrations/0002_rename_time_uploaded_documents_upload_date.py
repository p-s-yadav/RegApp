# Generated by Django 4.2.4 on 2023-08-29 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documents',
            old_name='time_uploaded',
            new_name='upload_date',
        ),
    ]
