from django.views.generic.list import ListView # type: ignore
from django.views.generic.detail import DetailView # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CharacterForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CharacterSerializer

from .models import Character, Background, CharacterClass, Skill

CHARACTER_FORM_FIELDS = ['character_name', 'character_class', 'subclass', 'race', 'level', 'background', 'alignment', 'experience_points', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'initiative', 'speed', 'hit_points', 'temporary_hit_points', 'hit_dice', 'death_saves_success', 'death_saves_failure', 'backstory', 'inspiration', 'languages']

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

        character = self.object

        # Inventory
        inventory = character.inventory.all()
        context['inventory'] = inventory
        context['current_ac'] = character.total_armor_class
        context['total_weight'] = sum(
            item.item.weight * item.quantity for item in inventory
        )

        # 👇 BACKGROUND OBJECT (NOWE)
        background_obj = Background.objects.filter(
            name=character.background
        ).first()
        context['background_obj'] = background_obj

        context['skill_proficiencies'] = character.get_skill_proficiencies()

        skills_data = []
        for skill in Skill.objects.all():
            skills_data.append({
                "skill": skill,
                "ability": skill.get_ability_display(),
                "is_proficient": skill in character.get_skill_proficiencies(),
                "bonus": character.get_skill_bonus(skill),
            })

        context["skills_data"] = skills_data

        return context

class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self._save_skills(form)
        return response

    def _save_skills(self, form):
        from .models import CharacterSkillProficiency

        CharacterSkillProficiency.objects.filter(
            character=self.object
        ).delete()

        for skill in form.cleaned_data.get("skills", []):
            CharacterSkillProficiency.objects.create(
                character=self.object,
                skill=skill
            )

class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'base/character_form.html'
    success_url = reverse_lazy('characters')

class CharacterCreateView(APIView):
    def post(self, request):
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def form_valid(self, form):
        response = super().form_valid(form)
        self._save_skills(form)
        return response

    def _save_skills(self, form):
        from .models import CharacterSkillProficiency

        CharacterSkillProficiency.objects.filter(
            character=self.object
        ).delete()

        for skill in form.cleaned_data.get("skills", []):
            CharacterSkillProficiency.objects.create(
                character=self.object,
                skill=skill
            )

class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'base/character_confirm_delete.html'
    success_url = reverse_lazy('characters')


from django.http import JsonResponse
from .models import Subclass

def subclasses_for_class(request):
    class_id = request.GET.get("class_id")
    subclasses = Subclass.objects.filter(character_class_id=class_id)
    data = [{"id": s.id, "name": s.name} for s in subclasses]
    return JsonResponse(data, safe=False)


def skills_for_class(request):
    class_id = request.GET.get("class_id")
    try:
        char_class = CharacterClass.objects.get(pk=class_id)
        skills = Skill.objects.filter(classskillchoice__character_class=char_class)
        data = [{"id": s.id, "name": s.name} for s in skills]
    except CharacterClass.DoesNotExist:
        data = []
    return JsonResponse(data, safe=False)