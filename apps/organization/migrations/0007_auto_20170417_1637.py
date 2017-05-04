# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 16:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20170417_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='\u6536\u85cf\u6570'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='points',
            field=models.CharField(default='', max_length=50, verbose_name='\u6559\u5b66\u7279\u70b9'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(default='', max_length=50, verbose_name='\u516c\u53f8\u804c\u4f4d'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(default='', max_length=50, verbose_name='\u5c31\u804c\u516c\u53f8'),
        ),
    ]