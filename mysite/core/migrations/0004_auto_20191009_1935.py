# Generated by Django 2.1.3 on 2019-10-09 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191009_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='todolist',
        ),
        migrations.DeleteModel(
            name='ToDoList',
        ),
    ]
