# Generated by Django 2.2.2 on 2019-12-01 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191201_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userfollowers', to=settings.AUTH_USER_MODEL),
        ),
    ]
