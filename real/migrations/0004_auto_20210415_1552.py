# Generated by Django 3.1.3 on 2021-04-15 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('real', '0003_auto_20210415_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realbar',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]