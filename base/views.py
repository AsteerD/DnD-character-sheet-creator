from django.views.generic.list import ListView # type: ignore
from django.views.generic.detail import DetailView # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Character, InventoryItem, Item

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


class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = context['characters'].filter(user=self.request.user)
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['characters'] = context['characters'].filter(character_name__istartswith=search_input)
        context['search_input'] = search_input
        return context

class CharacterDetail(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'base/character.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory = self.object.inventory.all()
        context['inventory'] = inventory
        
        total_weight = sum(item.item.weight * item.quantity for item in inventory)
        context['total_weight'] = total_weight
        return context

class CharacterCreate(LoginRequiredMixin,CreateView):
    model = Character
    fields = ['character_name', 'character_class', 'subclass', 'race', 'level', 'background', 'alligment', 'experience_points', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'armor_class', 'initiative', 'speed', 'hit_points', 'temporary_hit_points', 'hit_dice', 'death_saves_success', 'death_saves_failure', 'backstory', 'inspiration', 'languages']
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        character = self.object

        self.assign_starting_items(character)
        
        return response

    def assign_starting_items(self, character):
        starter_packs = {
            'Barbarian': [('Greataxe', 7.0), ('Handaxe', 2.0), ('Explorer\'s Pack', 5.0), ('Javelin', 2.0)],
            'Bard': [('Rapier', 2.0), ('Entertainer\'s Pack', 5.0), ('Lute', 2.0), ('Leather Armor', 10.0), ('Dagger', 1.0)],
            'Cleric': [('Mace', 4.0), ('Scale Mail', 45.0), ('Light Crossbow', 5.0), ('Shield', 6.0), ('Holy Symbol', 1.0)],
            'Fighter': [('Chain Mail', 55.0), ('Longsword', 3.0), ('Shield', 6.0), ('Light Crossbow', 5.0), ('Dungeoneer\'s Pack', 10.0)],
            'Monk': [('Shortsword', 2.0), ('Dart', 0.25)],
            'Paladin': [('Longsword', 3.0), ('Shield', 6.0), ('Chain Mail', 55.0), ('Holy Symbol', 1.0)],
            'Ranger': [('Scale Mail', 45.0), ('Shortsword', 2.0), ('Longbow', 2.0), ('Dungeoneer\'s Pack', 10.0)],
            'Rogue': [('Rapier', 2.0), ('Shortbow', 2.0), ('Leather Armor', 10.0), ('Dagger', 1.0), ('Thieves\' Tools', 1.0)],
            'Sorcerer': [('Light Crossbow', 5.0), ('Component Pouch', 2.0), ('Dagger', 1.0)],
            'Warlock': [('Light Crossbow', 5.0), ('Component Pouch', 2.0), ('Leather Armor', 10.0), ('Dagger', 1.0)],
            'Wizard': [('Quarterstaff', 4.0), ('Component Pouch', 2.0), ('Scholar\'s Pack', 10.0), ('Spellbook', 3.0)],
        }

        items_data = starter_packs.get(character.character_class, [])

        for item_name, item_weight in items_data: 
            item_obj, created = Item.objects.get_or_create(
                name=item_name,
                defaults={
                    'item_type': 'gear', 
                    'weight': item_weight,
                    'description': f'Standard starting equipment for {character.character_class}.'
                }
            )
            
            InventoryItem.objects.create(
                character=character,
                item=item_obj,
                quantity=1
            )

class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    fields = '__all__'
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'base/character_confirm_delete.html'
    success_url = reverse_lazy('characters')

