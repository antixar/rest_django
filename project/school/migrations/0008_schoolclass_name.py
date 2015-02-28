# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_schoolclass_cname'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='name',
            field=models.CharField(default=b'1a', max_length=64),
            preserve_default=True,
        ),
    ]
