# Generated by Django 4.2.5 on 2023-09-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_rename_angleoneobj_configuration_angleoneaccesstoken_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strategy',
            old_name='LotCondition',
            new_name='LotConditionG',
        ),
        migrations.AddField(
            model_name='strategy',
            name='LotConditionL',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
