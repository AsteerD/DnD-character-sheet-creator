from django.shortcuts import render # type: ignore
from django.views.generic.list import ListView # type: ignore
from django.views.generic.detail import DetailView # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView # type: ignore
from django.urls import reverse_lazy # type: ignore
from .models import Character

class CharacterList(ListView):
    model = Character
    context_object_name = 'characters'

class CharacterDetail(DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character.html'

class CharacterCreate(CreateView):
    model = Character
    fields = '__all__'
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

class CharacterUpdate(UpdateView):
    model = Character
    fields = '__all__'
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

class CharacterDelete(DeleteView):
    model = Character
    template_name = 'base/character_confirm_delete.html'
    success_url = reverse_lazy('characters')

class CharacterDelete(DeleteView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character_confirm_delete.html'
    success_url = reverse_lazy('characters')