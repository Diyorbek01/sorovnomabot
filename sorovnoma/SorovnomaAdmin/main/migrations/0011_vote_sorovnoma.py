# Generated by Django 4.1.7 on 2023-03-04 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_requiredchannel_tg_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='sorovnoma',
            field=models.ForeignKey(default=17, on_delete=django.db.models.deletion.CASCADE, related_name='voting', to='main.sorovnoma'),
            preserve_default=False,
        ),
    ]
