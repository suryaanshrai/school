# Generated by Django 4.2.2 on 2023-07-24 07:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_user_is_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard', models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(6)])),
                ('section', models.CharField(max_length=1, validators=[student.models.validate_section])),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=150)),
                ('marks', models.IntegerField()),
                ('max_marks', models.IntegerField()),
                ('date', models.DateField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.result')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=150)),
                ('due_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField(max_length=2000)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('issued_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.classroom')),
            ],
        ),
    ]
