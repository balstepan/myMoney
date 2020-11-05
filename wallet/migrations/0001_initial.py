# Generated by Django 3.1.2 on 2020-10-22 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Balance')),
                ('currency', models.CharField(choices=[('BYN', 'Belarus Ruble'), ('RUB', 'Russian Ruble'), ('USD', 'United States Dollar'), ('EUR', 'Euro')], default='BYN', max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_from', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount from')),
                ('value_to', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount to')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_from', to='wallet.account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_to', to='wallet.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('slug', models.SlugField(max_length=80)),
                ('color', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=250, verbose_name='Note')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('currency', models.CharField(choices=[('BYN', 'Belarus Ruble'), ('RUB', 'Russian Ruble'), ('USD', 'United States Dollar'), ('EUR', 'Euro')], default='BYN', max_length=30)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incomes', to='wallet.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.incomecategory', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('slug', models.SlugField(max_length=80)),
                ('color', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='wallet.costcategory', verbose_name='Parent category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=250, verbose_name='Note')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('currency', models.CharField(choices=[('BYN', 'Belarus Ruble'), ('RUB', 'Russian Ruble'), ('USD', 'United States Dollar'), ('EUR', 'Euro')], default='BYN', max_length=30)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='costs', to='wallet.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.costcategory', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
