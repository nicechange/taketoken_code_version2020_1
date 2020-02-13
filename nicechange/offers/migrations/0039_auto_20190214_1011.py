# Generated by Django 2.1.1 on 2019-02-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0038_auto_20190212_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='proffer',
            name='bank_yandex',
            field=models.BooleanField(default=False, verbose_name='Яндекс.Деньги'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='bank_search',
            field=models.CharField(choices=[('Сбербанк', 'Сбербанк'), ('Тинькофф', 'Тинькофф'), ('Втб-24', 'Втб-24'), ('Промсвязьбанк', 'Промсвязьбанк'), ('Альфабанк', 'Альфабанк'), ('Яндекс.Деньги', 'Яндекс.Деньги'), ('Qiwi', 'Qiwi')], default='Сбербанк', max_length=30, verbose_name='Способ оплаты'),
        ),
    ]
