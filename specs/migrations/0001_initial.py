# Generated by Django 4.0 on 2022-01-30 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=50, verbose_name='Имя ключа для категории')),
                ('feature_filter_name', models.CharField(max_length=50, verbose_name='Имя для фильтра')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='Единица измерения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
            ],
            options={
                'unique_together': {('category', 'feature_name', 'feature_filter_name')},
            },
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Характеристика')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_feature_value', models.CharField(max_length=100, verbose_name='Валидное значение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Ключ характеристики')),
            ],
        ),
    ]
