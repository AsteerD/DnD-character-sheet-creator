from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Character, Subclass, Feat
from .forms import CharacterForm

# --- LOGOWANIE I REJESTRACJA ---

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('characters')

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
            return redirect('characters')
        return super(RegisterPage, self).get(*args, **kwargs)

# --- WIDOKI POSTACI ---

class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pokazujemy tylko postacie zalogowanego użytkownika
        context['characters'] = context['characters'].filter(user=self.request.user)
        context['count'] = context['characters'].count()
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

    # Przekazujemy listę Featów do szablonu (dla prawej kolumny)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_feats'] = Feat.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CharacterCreate, self).form_valid(form)

class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

    # Przekazujemy listę Featów do szablonu (dla prawej kolumny)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_feats'] = Feat.objects.all()
        return context

# TEGO BRAKOWAŁO I DLATEGO MIAŁEŚ BŁĄD:
class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    context_object_name = 'character'
    success_url = reverse_lazy('characters')


# --- AJAX (DYNAMICZNE PODKLASY) ---

def ajax_load_subclasses(request):
    class_id = request.GET.get('class_id')
    if class_id:
        subclasses = Subclass.objects.filter(character_class_id=class_id).order_by('name')
    else:
        subclasses = Subclass.objects.none()
    return render(request, 'base/subclass_dropdown_list_options.html', {'subclasses': subclasses})