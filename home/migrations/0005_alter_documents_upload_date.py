# Generated by Django 4.2.4 on 2023-09-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_documents_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
