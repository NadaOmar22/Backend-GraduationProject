# Generated by Django 4.1.7 on 2023-05-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacilityApp', '0003_alter_app_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/'),
        ),
        migrations.AlterField(
            model_name='app',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]