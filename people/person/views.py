from django.shortcuts import render
from .models import Person
# Create your views here.
from django.views import generic

class PersonListView(generic.ListView):
    model = Person

class PersonDetailView(generic.DetailView):
    model = Person
