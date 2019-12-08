# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workbookchapter',
            name='workbook_chapter_name',
            field=models.CharField(max_length=100, verbose_name='章节名'),
        ),
    ]
