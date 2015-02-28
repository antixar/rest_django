# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20150228_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolclass',
            name='pupil',
        ),
    ]
