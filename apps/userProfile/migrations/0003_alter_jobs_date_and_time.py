# Generated by Django 3.2 on 2024-11-28 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_alter_jobs_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='date_and_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]