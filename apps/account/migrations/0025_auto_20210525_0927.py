# Generated by Django 3.2 on 2021-05-25 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0001_initial'),
        ('account', '0024_alter_worker_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerworker',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.position', verbose_name='worker position'),
        ),
        migrations.AlterField(
            model_name='subworker',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.position', verbose_name='worker position'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='position',
            field=models.ForeignKey(blank=True, limit_choices_to={'status': 0}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_workers', to='position.position', verbose_name='worker position'),
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]
