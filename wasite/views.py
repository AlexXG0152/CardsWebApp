from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import Max, Min

from .models import Card, Purchases
from .tables import CardTable, PurchasesTable
from .forms import CardEditForm, GenerateCards, AuthorListFormHelper
from .filters import CardFilter
from .utils import card_generator, card_generator_dicts, PagedFilteredTableView

from django_tables2 import SingleTableView


@login_required
def index(request):
    """Home page"""
    return render(request, 'wasite/index.html')


def update_view(request, id):
    """Page for update card data (activate, delete etc.)"""
    # dictionary for initial data with field names as keys
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Card, id = id)
    # pass the object as instance in form
    form = CardEditForm(request.POST or None, instance = obj)
    # save the data from the form and redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/cards/")
    # add form dictionary to context
    context["form"] = form
    return render(request, "wasite/card_edit.html", context)


class CardListView(PagedFilteredTableView, SingleTableView):
    """Show all cards table"""
    model = Card
    table_class = CardTable
    filter_class = CardFilter
    formhelper_class = AuthorListFormHelper
    template_name = 'wasite/cards.html'
    paginate_by = 50


class CardDetailView(DetailView):
    """Show card details (Purchases table)"""
    model = Card
    table_class = PurchasesTable
    template_name = 'wasite/card.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CardDetailView, self).get_context_data(*args, **kwargs)
        card = Card.objects.all()
        context['table'] = card
        purchases = Purchases.objects.filter(card_id=self.get_object()).order_by('-date_create')
        context['purchases'] = purchases
        return context

@login_required
def purchase_info(request, purchase_id):
    """Show page with one purchase transaction details info"""
    context = {}
    purchase = Purchases.objects.filter(id = purchase_id)
    context["purchase"] = purchase
    return render(request, "wasite/purchases.html", context)


@login_required
def generate(request, page=1):
    """Generate and send to DB generated card"""
    if request.method == "POST":
        if 'generate' in request.POST:
            form = GenerateCards(request.POST)
            if form.is_valid():
                series = form.cleaned_data["series"]
                quantity = form.cleaned_data["quantity"]
                status = form.cleaned_data["status"]
                period = form.cleaned_data["period"]
                start = 0
                context = {"form":form}
                if Card.objects.filter(series = form.cleaned_data["series"], number = "99999").exists():
                    context.update({'message':"This series already exists"})
                if Card.objects.filter(series = form.cleaned_data["series"], number = "00001").exists():
                    last_exist_num_card = Card.objects.filter(series = form.cleaned_data["series"]).aggregate(Max("number"))
                    start = int(last_exist_num_card['number__max'])
                cards = card_generator(series, quantity, status, period, start)
                context.update({'cards':cards})
                return render (request, "wasite/generate.html", context)
        if 'send_to_db' in request.POST:
            form = GenerateCards(request.POST)
            if form.is_valid():
                series = form.cleaned_data["series"]
                quantity = form.cleaned_data["quantity"]
                status = form.cleaned_data["status"]
                period = form.cleaned_data["period"]
                start = 0
                if Card.objects.filter(series = form.cleaned_data["series"]).exists() and Card.objects.filter(number = "00001").exists():
                    last_exist_num_card = Card.objects.filter(series = form.cleaned_data["series"]).aggregate(Max("number"))
                    start = int(last_exist_num_card['number__max'])
                cards = card_generator_dicts(series, quantity, status, period, start)
                context = {"form":form}
                obj_list = [Card(**data_dict) for data_dict in cards]
                objs = Card.objects.bulk_create(obj_list)
                context.update({"success":"Cards succefully added!"})
                return render (request, "wasite/generate.html", context)
    else:
        form = GenerateCards()
        exists_card = Card.objects.values("series").order_by("series").annotate(total=Min("number"), total2=Max("number"))
        context = {"form":form}
        context.update({'exists_card':exists_card})
        return render(request, "wasite/generate.html", context)
