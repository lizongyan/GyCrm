# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-14 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170407_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u8001\u5e08\u540d')),
                ('work_years', models.IntegerField(default=0, verbose_name='\u5de5\u4f5c\u5e74\u9650')),
                ('work_company', models.CharField(max_length=50, verbose_name='\u5c31\u804c\u516c\u53f8')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u6240\u5c5e\u673a\u6784')),
            ],
        ),
        migrations.AlterField(
            model_name='citydict',
            name='name',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=20, unique=True, verbose_name='\u57ce\u5e02'),
        ),
    ]
