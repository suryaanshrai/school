# Generated by Django 4.2.2 on 2023-08-30 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_penalty_book_penalty_date_of_return_penalty_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='penalty',
            name='due_date',
        ),
    ]
