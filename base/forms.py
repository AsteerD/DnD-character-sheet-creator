from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Character, Spell
import math

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        # Tutaj 'exclude' zadziała poprawnie
        exclude = ['user', 'spells']

class SpellSelectionForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['spells']
        widgets = {
            'spells': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        character = self.instance

        if character and character.pk:
            # 1. Pobieramy klasę i poziom
            char_class = character.character_class.name
            char_level = character.level
            
            # 2. Obliczamy MAX Spell Tier
            max_spell_tier = 0
            
            # Half-Casters
            if char_class in ['Paladin', 'Ranger']:
                if char_level >= 17: max_spell_tier = 5
                elif char_level >= 13: max_spell_tier = 4
                elif char_level >= 9: max_spell_tier = 3
                elif char_level >= 5: max_spell_tier = 2
                elif char_level >= 2: max_spell_tier = 1
                else: max_spell_tier = 0
            
            # Full-Casters + Warlock (uproszczone)
            else:
                max_spell_tier = math.ceil(char_level / 2.0)
                if max_spell_tier > 9: max_spell_tier = 9

            # 3. Filtrowanie
            self.fields['spells'].queryset = Spell.objects.filter(
                available_to_classes__name=char_class,
                level__lte=max_spell_tier
            ).order_by('level', 'name')
            
            self.fields['spells'].label = ""