# Generated by Django 4.1.1 on 2022-11-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0007_alter_total_yukyu_name_alter_total_yukyu_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='total_yukyu',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='yearwage',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='zangyo',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]