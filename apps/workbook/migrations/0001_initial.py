# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workbook',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('workbook_name', models.CharField(null=True, verbose_name='练习册名', max_length=30, blank=True)),
                ('subject', models.CharField(null=True, verbose_name='科目', max_length=20, blank=True)),
                ('grade', models.CharField(null=True, verbose_name='年级', max_length=20, blank=True)),
            ],
            options={
                'verbose_name': '练习册',
                'verbose_name_plural': '练习册',
                'db_table': 'workbook',
            },
        ),
        migrations.CreateModel(
            name='WorkbookChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('workbook_chapter_name', models.CharField(max_length=40, verbose_name='章节名')),
                ('workbook', models.ForeignKey(verbose_name='练习册id', to='workbook.Workbook')),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节',
                'db_table': 'workbook_chapter',
            },
        ),
    ]
