# Generated by Django 4.1.1 on 2022-11-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0004_alter_total_yukyu_options_alter_wage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='total_yukyu',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wage',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yearwage',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zangyo',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
