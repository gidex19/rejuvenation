# Generated by Django 2.2.2 on 2019-09-06 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redcloud', '0007_post_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date_posted',)},
        ),
    ]
