from .models import *
import django_filters


class CardFilter(django_filters.FilterSet):
    class Meta:
        model = Card
        fields = ['id', 'series', 'number', 'date_start', 'date_start',
                  'date_end', 'date_delete', 'period', 'status']
