# booking/views/cake_views.py
from django.views.generic import ListView, DetailView
from ..models import Cake

class CakeListView(ListView):
    model = Cake
    context_object_name = 'cakes'
    template_name = 'cakes/cake_list.html'

class CakeDetailView(DetailView):
    model = Cake
    context_object_name = 'cake'
    template_name = 'cakes/cake_detail.html'
