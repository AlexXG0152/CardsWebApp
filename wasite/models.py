from dateutil.relativedelta import relativedelta
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
import datetime


class Card(models.Model):
    """ 
    DB with info about cards.
    Card status and card valid period choices from dropdown list. 
    This is prevent user mistakes and been in brief.
    After any edit and save operation DB automatically check and clean data in rows
    (card status etc.)

    """
    
    CARD_STATUS = (
        ('0', 'Not activated'),
        ('1', 'Activated'),
        ('2', 'Expired'),
        ('3', 'Deleted'),
    )

    CARD_PERIOD = (
        ('1','1 month'),
        ('6','6 months'),
        ('12','12 months'),
        )
    
    series = models.CharField(max_length=2)
    number = models.CharField(max_length=5)
    date_create = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_delete = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=CARD_STATUS)
    period = models.CharField(max_length=3, choices=CARD_PERIOD)

    def get_absolute_url(self):
        return reverse('card', kwargs={'pk': self.id})
    
    def clean(self):
        if self.date_start is not None and self.status == '0':
            self.date_end = self.date_start + relativedelta(months=int(self.period))
            self.status = '1'
        if self.date_start is None and self.status != '0':
            self.status = '0'
        if self.date_start is not None and self.status == '1':
            self.date_end = self.date_start + relativedelta(months=int(self.period))
        if self.date_end.replace(tzinfo=None) < datetime.datetime.now() - datetime.timedelta(seconds=20):
            self.status = '2'
        if (datetime.datetime.now() - datetime.timedelta(seconds=20)) < self.date_end.replace(tzinfo=None) and self.status in ['0', '1']:
            self.status = '1'
    
    def __str__(self):
        return self.series + self.number


class Purchases(models.Model):
    """
    DB with purchases examples. Create automatically from generate_purchases.py file.
    """
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    card = models.CharField(max_length=7)
    date_create = models.DateTimeField(blank=True, null=True)
    summ = models.FloatField(default=0)
    goods = models.CharField(max_length=100000)
    shop = models.IntegerField()
    emploeye = models.IntegerField()

    def __str__(self):
        return self.id, self.card_id, self.card, self.date_create, self.summ, self.goods, self.shop, self.emploeye
