# Generated by Django 5.0.6 on 2025-05-01 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_alter_feedbackres_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.batch'),
        ),
    ]
