# Generated by Django 2.2.2 on 2019-12-01 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userfollowers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='usr',
        ),
        migrations.RenameField(
            model_name='userfollowers',
            old_name='user',
            new_name='usr',
        ),
    ]
