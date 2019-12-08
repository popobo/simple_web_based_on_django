# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_userquestionimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userquestionimage',
            options={'verbose_name_plural': '用户上传的题目图片', 'verbose_name': '用户上传的题目图片'},
        ),
        migrations.AlterModelTable(
            name='userquestionimage',
            table='user_question_image',
        ),
    ]
