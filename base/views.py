from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.views.generic.list import ListView # type: ignore
from django.views.generic.detail import DetailView # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView # type: ignore
from django.urls import reverse_lazy # type: ignore
from .models import Character
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SpellSelectionForm, CharacterForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('characters')

class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_queryset(self):
        # Pokazuje tylko postacie zalogowanego użytkownika
        return Character.objects.filter(user=self.request.user)

class CharacterDetail(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character.html'

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm  # <--- KLUCZOWA ZMIANA
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CharacterCreate, self).form_valid(form)

class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm  # <--- KLUCZOWA ZMIANA
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')
    
    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character_confirm_delete.html'
    success_url = reverse_lazy('characters')

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

# --- Widok Zarządzania Czarami ---

@login_required
def character_spells(request, pk):
    character = get_object_or_404(Character, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SpellSelectionForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect('character', pk=character.pk) 
    else:
        form = SpellSelectionForm(instance=character)

    context = {
        'form': form,
        'character': character
    }
    return render(request, 'base/character_spells.html', context)