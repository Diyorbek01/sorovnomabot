# Generated by Django 4.1.7 on 2023-02-25 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RequiredChannels',
            new_name='RequiredChannel',
        ),
    ]