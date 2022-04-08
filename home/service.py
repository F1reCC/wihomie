import django_filters

from product.models import Variants

class CharFilterInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class ProductFilter(django_filters.FilterSet):

    size = CharFilterInFilter(field_name='size__name', lookup_expr='in')
    color = CharFilterInFilter(field_name='color__name', lookup_expr='in')
    price = django_filters.NumberFilter()
    
    class Meta:
        model = Variants
        fields = {
            'price', 'color', 'size'
        }