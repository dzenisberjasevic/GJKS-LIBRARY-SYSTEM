# Generated by Django 5.0.6 on 2024-05-29 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.IntegerField(default=1, max_length=200),
        ),
    ]
