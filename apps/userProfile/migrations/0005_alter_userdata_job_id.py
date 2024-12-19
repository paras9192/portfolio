# Generated by Django 3.2 on 2024-12-04 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0004_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to='userProfile.jobs', unique=True),
        ),
    ]