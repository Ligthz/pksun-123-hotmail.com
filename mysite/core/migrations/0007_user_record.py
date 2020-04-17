# Generated by Django 2.2 on 2020-04-10 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200404_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_ID', models.CharField(max_length=30)),
                ('Role', models.CharField(max_length=20)),
                ('last_seen', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
