# Generated by Django 3.2 on 2024-11-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='IN_PROGRESS', max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('date_and_time', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Jobs',
            },
        ),
    ]
