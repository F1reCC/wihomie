from django.contrib.auth.models import User
from django.db import models

from product.models import Product, Variants


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)


class Order(models.Model):
    STATUS_NEW = 'New'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_PREAPARING = 'Preaparing'
    STATUS_ONSHIPPING = 'OnShipping'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELED = 'Canceled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Поступил'),
        (STATUS_ACCEPTED, 'Принят'),
        (STATUS_PREAPARING, 'Подготовка'),
        (STATUS_ONSHIPPING, 'Отправлен'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_CANCELED, 'Отменён'),
    )

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_UKR_MAIL = 'ukr_mail'
    BUYING_TYPE_NEW_MAIL = 'new_mail'

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_UKR_MAIL, 'Доставка Новой почтой'),
        (BUYING_TYPE_NEW_MAIL, 'Доставка Укрпочтой')
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=7, editable=False )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default = STATUS_NEW)
    buying_type = models.CharField(max_length=50, verbose_name='Тип заказа', choices = BUYING_TYPE_CHOICES)
    paying_type = models.CharField(max_length=50, verbose_name='Вид оплаты')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    
    def __str__(self):
        return self.user.first_name

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'Новый'),
        ('Accepted', 'Принят'),
        ('Canceled', 'Отменён'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", null=True, blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title