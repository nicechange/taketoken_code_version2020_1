# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-14 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('privatemessages', '0008_threadactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFlags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagIsBalanceCorrect', models.BooleanField(db_index=True, default=True)),
                ('flagIsCryptaSended', models.BooleanField(db_index=True, default=False)),
                ('flagIsCryptaTaked', models.BooleanField(db_index=True, default=False)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='privatemessages.Thread')),
            ],
        ),
        migrations.RemoveField(
            model_name='dealrole',
            name='thread',
        ),
        migrations.RemoveField(
            model_name='dealrole',
            name='user',
        ),
        migrations.RemoveField(
            model_name='dealrole',
            name='wallet',
        ),
        migrations.DeleteModel(
            name='DealRole',
        ),
    ]
