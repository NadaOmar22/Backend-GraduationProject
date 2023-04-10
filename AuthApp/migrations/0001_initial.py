# Generated by Django 4.1.7 on 2023-03-21 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserId', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(default='Ali', max_length=100)),
                ('Email', models.EmailField(default='test@example.com', max_length=50)),
                ('Password', models.CharField(default='khjufgrtanb', max_length=128)),
                ('Gender', models.CharField(default='male', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AuthApp.user')),
                ('PhoneNumber', models.CharField(default='01128336553', max_length=12)),
            ],
            bases=('AuthApp.user',),
        ),
    ]
