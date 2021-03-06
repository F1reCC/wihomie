# Generated by Django 4.0 on 2022-01-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=5)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=20)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'Поступил'), ('Accepted', 'Принят'), ('Preaparing', 'Подготовка'), ('OnShipping', 'Отправлен'), ('Completed', 'Завершен'), ('Canceled', 'Отменён')], default='New', max_length=10)),
                ('buying_type', models.CharField(choices=[('self', 'Самовывоз'), ('ukr_mail', 'Доставка Новой почтой'), ('new_mail', 'Доставка Укрпочтой')], max_length=50, verbose_name='Тип заказа')),
                ('paying_type', models.CharField(max_length=50, verbose_name='Вид оплаты')),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('adminnote', models.CharField(blank=True, max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'Новый'), ('Accepted', 'Принят'), ('Canceled', 'Отменён')], default='New', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
