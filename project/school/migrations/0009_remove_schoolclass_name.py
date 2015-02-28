# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_schoolclass_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolclass',
            name='name',
        ),
    ]
