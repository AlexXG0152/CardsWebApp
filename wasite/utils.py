from django_tables2 import SingleTableView


class PagedFilteredTableView(SingleTableView):
    """Filter for cards table"""
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


def card_generator(series, quantity, status, period, start=1):
    """card generator for show on page for  range of users generated cards"""
    
    card_generator = [[series, f"0000{i}"[-5:], str(status), str(period)] for i in range(start+1, int(quantity)+(start+1))]
    return card_generator


def card_generator_dicts(series, quantity, status, period, start=1):
    """card generator for generate and send to DB range of users generated cards"""

    keys = ['series', 'number', 'status', 'period']
    card_generator_dict = [(series, f"0000{i}"[-5:], str(status), str(period)) for i in range(start+1, int(quantity)+(start+1))]
    result = [dict(zip(keys, i)) for i in card_generator_dict]
    return result