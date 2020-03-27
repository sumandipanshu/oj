# Generated by Django 2.2.5 on 2019-10-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(default='processing', max_length=10),
            preserve_default=False,
        ),
    ]
