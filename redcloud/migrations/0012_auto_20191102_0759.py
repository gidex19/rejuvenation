# Generated by Django 2.2.2 on 2019-11-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redcloud', '0011_auto_20190907_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date_posted',)},
        ),
        migrations.AddField(
            model_name='post',
            name='image_post',
            field=models.ImageField(default='default.jpg', upload_to='post_pics'),
        ),
    ]