# Generated by Django 3.2 on 2024-11-28 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='description',
            field=models.CharField(default='System Generate Job Description', max_length=200),
        ),
    ]
