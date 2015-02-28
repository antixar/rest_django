# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_remove_person_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='pupil',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
        migrations.AlterField(
            model_name='schoolclass',
            name='teacher',
            field=models.ForeignKey(to='school.Person'),
            preserve_default=True,
        ),
    ]
