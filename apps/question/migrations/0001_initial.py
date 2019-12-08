# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('content', models.CharField(null=True, verbose_name='题目内容', max_length=3500, blank=True)),
                ('answer', models.CharField(null=True, verbose_name='题目答案', max_length=1000, blank=True)),
                ('picture_path', models.CharField(null=True, verbose_name='题目图片存储路径', max_length=100, blank=True)),
                ('grade', models.CharField(max_length=20, verbose_name='年级')),
                ('subject', models.CharField(null=True, verbose_name='科目', max_length=20, blank=True)),
                ('type', models.CharField(null=True, verbose_name='类型', max_length=20, blank=True)),
                ('workbook', models.ForeignKey(null=True, to='workbook.Workbook', blank=True)),
                ('workbook_chapter', models.ForeignKey(null=True, to='workbook.WorkbookChapter', blank=True)),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='SubImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('sub_image_path', models.CharField(max_length=100, verbose_name='小题图片路径')),
                ('question', models.ForeignKey(verbose_name='题目id', to='question.Question')),
            ],
            options={
                'verbose_name': '小题图片',
                'verbose_name_plural': '小题图片',
                'db_table': 'sub_image',
            },
        ),
    ]
