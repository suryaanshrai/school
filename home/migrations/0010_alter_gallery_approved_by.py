# Generated by Django 4.2.2 on 2023-07-28 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_remove_gallery_active_event_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='approved_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
