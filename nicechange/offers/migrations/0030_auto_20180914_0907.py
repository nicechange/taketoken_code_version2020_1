# Generated by Django 2.1.1 on 2018-09-14 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('privatemessages', '0009_auto_20180214_1750'),
        ('offers', '0029_auto_20180420_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveDeals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='privatemessages.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinishedDeals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('partner', models.CharField(max_length=30, verbose_name='Покупатель/Продавец')),
                ('price', models.FloatField(default=0, max_length=200, verbose_name='Сумма')),
                ('status', models.CharField(default='Sent', max_length=30, verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='proffer',
            name='bank',
            field=models.CharField(choices=[('Сбербанк', 'Сбербанк'), ('Тинькофф', 'Тинькофф'), ('Втб-24', 'Втб-24'), ('Промсвязьбанк', 'Промсвязьбанк')], default='Сбербанк', max_length=30, verbose_name='Банк'),
        ),
        migrations.AlterField(
            model_name='course',
            name='sellorbuy',
            field=models.CharField(choices=[('ПРОДАЖА', 'ПРОДАЖА'), ('ПОКУПКА', 'ПОКУПКА')], default='ПРОДАЖА', max_length=30, null=True, unique=True, verbose_name='Продать/купить'),
        ),
        migrations.AlterField(
            model_name='course',
            name='type_of_token',
            field=models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH')], default='BTC', max_length=30, verbose_name='Крипта'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='information',
            field=models.CharField(max_length=30, null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(default='Sent', max_length=30, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='order',
            name='offers_count',
            field=models.IntegerField(default=0, verbose_name='Количество сделок'),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(default='Draft', max_length=30, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='rate',
            field=models.FloatField(default=0, max_length=200, verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='replies_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во ответов'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='state',
            field=models.CharField(default='Draft', max_length=30, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='type',
            field=models.CharField(choices=[('КУПЛЮ', 'КУПЛЮ'), ('ПРОДАМ', 'ПРОДАМ')], default='КУПЛЮ', max_length=30, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='proffer',
            name='type_of_token',
            field=models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH'), ('DASH', 'DASH'), ('ZEC', 'ZEC'), ('XMR', 'XMR')], default='BTC', max_length=30, verbose_name='Крипта'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='status',
            field=models.CharField(default='Sent', max_length=30, verbose_name='Статус'),
        ),
    ]
