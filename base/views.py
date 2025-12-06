from django.shortcuts import render # type: ignore
from django.views.generic.list import ListView # type: ignore
from django.views.generic.detail import DetailView # type: ignore
from .models import Character

class CharacterList(ListView):
    model = Character
    context_object_name = 'characters'

class CharacterDetail(DetailView):
    model = Character
    context_object_name = 'character'