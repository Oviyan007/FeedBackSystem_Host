# Generated by Django 5.0.6 on 2024-10-17 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_feedbackres_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackres',
            name='staff',
        ),
    ]