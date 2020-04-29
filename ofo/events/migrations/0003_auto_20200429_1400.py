# Generated by Django 3.0.5 on 2020-04-29 14:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20200422_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comment',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='guests',
            field=models.ManyToManyField(related_name='guests', to=settings.AUTH_USER_MODEL),
        ),
    ]