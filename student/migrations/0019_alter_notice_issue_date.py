# Generated by Django 4.2.2 on 2023-08-30 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_alter_notice_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='issue_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 30, 16, 8, 10, 463793)),
        ),
    ]
