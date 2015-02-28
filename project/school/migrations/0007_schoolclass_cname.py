# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_remove_schoolclass_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='cname',
            field=models.CharField(default=b'1a', max_length=64),
            preserve_default=True,
        ),
    ]
