#-*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView

from mailer.models import Company, Contact

from django.core.paginator import Paginator

from django.db.models import Prefetch, Sum, Count

contacts_with_orders = Prefetch(
    'contacts',
    queryset=Contact.objects.annotate(order_count=Count('orders'))
)

company_list = (Company.objects
    .prefetch_related(contacts_with_orders)
    .annotate(order_sum=Sum('orders__total'),
              order_count=Count('orders'))
)

class IndexView(ListView):
    template_name = "mailer/index.html"
    model = Company
    paginate_by = 100
	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
		
        p = Paginator(company_list, self.paginate_by)
        context['company_list'] = p.page(context['page_obj'].number)
		
        return context