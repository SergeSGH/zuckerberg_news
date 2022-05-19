# Generated by Django 2.2.16 on 2022-05-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Рейтинг', max_digits=2, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='news',
            name='views',
            field=models.IntegerField(blank=True, help_text='Количество просмотров', verbose_name='Количество просмотров'),
        ),
    ]