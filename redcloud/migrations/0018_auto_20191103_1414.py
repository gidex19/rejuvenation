# Generated by Django 2.2.2 on 2019-11-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redcloud', '0017_post_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uploaded_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='posted_file'),
        ),
    ]
