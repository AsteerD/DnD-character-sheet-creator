from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Character
from .forms import CharacterForm
from .classes.rogue import Rogue
from .classes.cleric import Cleric

# --- AUTH VIEWS ---

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('character-list')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('character-list')
        return super(RegisterPage, self).get(*args, **kwargs)

# --- CHARACTER VIEWS ---

class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = context['characters'].filter(user=self.request.user)
        return context

class CharacterDetail(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character_detail.html'

class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        form.instance.user = self.request.user # Assign user
        self.object = form.save()

        selected_class = self.object.character_class.upper()
        selected_subclass = form.cleaned_data.get('subclass')

        if selected_class == 'ROGUE':
            Rogue.objects.create(character=self.object, subclass_type=selected_subclass)
        elif selected_class == 'CLERIC':
            Cleric.objects.create(character=self.object, domain=selected_subclass)

        return super().form_valid(form)

class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    success_url = reverse_lazy('characters')

class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    context_object_name = 'character'
    success_url = reverse_lazy('characters')