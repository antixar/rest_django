# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('birthday', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('pupil', models.ManyToManyField(related_name='pupil_class', to='school.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('blocked', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('subject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='school.Subject')),
            ],
            options={
            },
            bases=('school.subject',),
        ),
        migrations.AddField(
            model_name='subject',
            name='status',
            field=models.ForeignKey(to='school.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='status',
            field=models.ForeignKey(to='school.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='teacher',
            field=models.ForeignKey(related_name='teacher_class', to='school.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.ForeignKey(to='school.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.ManyToManyField(to='school.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='pupil',
            field=models.ForeignKey(related_name='journal_pupil', to='school.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='subject',
            field=models.ForeignKey(related_name='journal_subject', to='school.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journal',
            name='teacher',
            field=models.ForeignKey(related_name='journal_teacher', to='school.Person'),
            preserve_default=True,
        ),
    ]
