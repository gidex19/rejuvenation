# Generated by Django 2.2.2 on 2019-11-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redcloud', '0012_auto_20191102_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_post',
            field=models.ImageField(upload_to='post_pics'),
        ),
    ]
