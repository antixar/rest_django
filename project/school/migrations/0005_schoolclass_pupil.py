# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_remove_schoolclass_pupil'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='pupil',
            field=models.ManyToManyField(related_name='pupil_class', to='school.Person'),
            preserve_default=True,
        ),
    ]
