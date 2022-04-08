from msilib.schema import CheckBox
from django import forms
from .models import ShopCart, Order

PAYING_TYPE_CARD = 'card'
PAYING_TYPE_COD = 'cod'
PAYING_TYPE_CASH = 'cash'


PAYING_TYPE_CHOICES = (
    (PAYING_TYPE_CARD, 'Безналичный расчёт'),
    (PAYING_TYPE_COD, 'Наложенный платёж'),
    (PAYING_TYPE_CASH, 'Оплата наличными')
)

class OrderForm(forms.ModelForm):

    save_address = forms.CheckboxInput()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'buying_type', 'paying_type', 'city', 'phone', 'comment']
