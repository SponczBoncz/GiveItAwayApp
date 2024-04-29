# Generated by Django 4.2.7 on 2024-04-28 20:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0)),
                ('categories', models.ManyToManyField(to='my_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('zip_code', models.CharField(max_length=64)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('is_taken', models.BooleanField(default=False)),
                ('is_taken_changed_date', models.DateTimeField(blank=True, null=True)),
                ('categories', models.ManyToManyField(to='my_app.category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.institution')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
