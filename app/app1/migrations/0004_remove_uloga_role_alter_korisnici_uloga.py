# Generated by Django 4.2.1 on 2023-06-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_uloga_alter_korisnici_uloga'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uloga',
            name='role',
        ),
        migrations.AlterField(
            model_name='korisnici',
            name='uloga',
            field=models.CharField(choices=[('ADMIN', 'admin'), ('PROFESOR', 'profesor'), ('STUDENT', 'student')], max_length=50),
        ),
    ]
