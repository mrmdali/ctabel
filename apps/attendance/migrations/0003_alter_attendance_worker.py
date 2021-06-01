# Generated by Django 3.2 on 2021-05-20 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_worker_header_worker'),
        ('attendance', '0002_auto_20210517_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subworkers', to='account.worker', verbose_name='Worker'),
        ),
    ]
