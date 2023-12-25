# Generated by Django 5.0 on 2023-12-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='certificate_image',
            field=models.ImageField(default='images/avatar-default.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='provider',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
