# Generated by Django 3.2 on 2021-07-13 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0002_auto_20210714_0015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='door',
            options={'verbose_name': 'Door', 'verbose_name_plural': '    Doors'},
        ),
        migrations.AlterModelOptions(
            name='face',
            options={'verbose_name': 'Face', 'verbose_name_plural': ' Faces'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person', 'verbose_name_plural': '  Persons'},
        ),
        migrations.AlterModelOptions(
            name='terminal',
            options={'verbose_name': 'Terminal', 'verbose_name_plural': '   Terminals'},
        ),
    ]