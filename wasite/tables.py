import django_tables2 as tables
from .models import Card, Purchases
from django_tables2.utils import A 


class CardTable(tables.Table):
    """Table for show user cards from DB"""
    id = tables.TemplateColumn('<a href="/cards/{{record.id}}">{{record.id}}</a>')
    class Meta:
        model = Card
        per_page = 30
        template_name = "django_tables2/bootstrap4.html"


class PurchasesTable(tables.Table):
    """Table for show user purchases from DB"""
    id = tables.TemplateColumn('<a href="/cards/{{record.id}}">{{record.id}}</a>')
    class Meta:
        model = Purchases
        exclude = ('card_id',)
        per_page = 30
        template_name = "django_tables2/bootstrap4.html"
