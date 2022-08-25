from cProfile import label
from unicodedata import lookup
import django_filters

from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created",
                            lookup_expr="gte", 
                            label="Date Ordered is >=: (MM/DD/YYYY)")
    end_date = DateFilter(field_name="date_created",
                          lookup_expr="lte",
                          label="Date Ordered is <=: (MM/DD/YYYY)")
    note = CharFilter(field_name="note", lookup_expr="icontains")
    
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']