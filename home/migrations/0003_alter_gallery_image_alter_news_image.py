# Generated by Django 4.2.2 on 2023-07-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_gallery_approved_by_gallery_author_news_approved_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
