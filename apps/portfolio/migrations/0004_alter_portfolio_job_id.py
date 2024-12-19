# Generated by Django 3.2 on 2024-12-05 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0005_alter_userdata_job_id'),
        ('portfolio', '0003_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_portfolio', to='userProfile.jobs', unique=True),
        ),
    ]