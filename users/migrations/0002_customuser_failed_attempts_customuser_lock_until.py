# Generated by Django 5.1.5 on 2025-01-28 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='failed_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lock_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
