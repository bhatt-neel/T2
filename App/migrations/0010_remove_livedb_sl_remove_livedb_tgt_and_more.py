# Generated by Django 4.2.5 on 2023-10-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_livedb_remove_order_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livedb',
            name='SL',
        ),
        migrations.RemoveField(
            model_name='livedb',
            name='TGT',
        ),
        migrations.RemoveField(
            model_name='livedb',
            name='T_TGT',
        ),
        migrations.AlterField(
            model_name='livedb',
            name='BUYINGPRICE',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livedb',
            name='LTP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livedb',
            name='PNL',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livedb',
            name='Returns',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livedb',
            name='Strategy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
