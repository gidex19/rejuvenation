# Generated by Django 2.2.2 on 2019-09-07 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redcloud', '0010_auto_20190906_0802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_image',
        ),
    ]