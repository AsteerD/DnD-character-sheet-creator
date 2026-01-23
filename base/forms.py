# base/forms.py
from django import forms
from .models import Character, Skill, Subclass, CharacterClass, Spell
from django.core.exceptions import ValidationError

class CharacterForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Class Skill Proficiencies"
    )

    class Meta:
        model = Character
        fields = [
            'character_name',
            'character_class',
            'subclass',
            'race',
            'level',
            'background',
            'alignment',
            'experience_points',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'backstory',
            'inspiration',
            'languages',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("DEBUG: Initializing CharacterForm")
        print("DEBUG: instance.pk =", self.instance.pk)
        print("DEBUG: self.data =", self.data)

        # ----------------------
        # Subclasses
        # ----------------------
        if self.instance.pk and self.instance.character_class:
            # EDIT mode
            print("DEBUG: EDIT → filter subclasses for", self.instance.character_class)
            self.fields['subclass'].queryset = Subclass.objects.filter(
                character_class=self.instance.character_class
            )
        elif 'character_class' in self.data:
            # POST mode (class selected)
            try:
                class_id = int(self.data.get('character_class'))
                print("DEBUG: POST → filter subclasses for class_id", class_id)
                self.fields['subclass'].queryset = Subclass.objects.filter(
                    character_class_id=class_id
                )
            except (ValueError, TypeError):
                print("DEBUG: Invalid class_id", self.data.get('character_class'))
                self.fields['subclass'].queryset = Subclass.objects.none()
        else:
            # CREATE GET → show all subclasses
            print("DEBUG: CREATE GET → show all subclasses")
            self.fields['subclass'].queryset = Subclass.objects.all()

        # ----------------------
        # Skills
        # ----------------------
        char_class = None

        # Determine class for skills
        if self.instance.pk and self.instance.character_class:
            # EDIT
            char_class = self.instance.character_class
        elif 'character_class' in self.data:
            try:
                class_id = int(self.data.get('character_class'))
                char_class = CharacterClass.objects.get(pk=class_id)
            except (ValueError, TypeError, CharacterClass.DoesNotExist):
                char_class = None
        else:
            # CREATE GET → fallback to first class if exists
            char_class = CharacterClass.objects.first()

        if char_class:
            print("DEBUG: Setting skills queryset for class", char_class)
            self.fields['skills'].queryset = Skill.objects.filter(
                classskillchoice__character_class=char_class
            )
            if self.instance.pk:
                self.fields['skills'].initial = (
                    self.instance.characterskillproficiency_set.values_list('skill_id', flat=True)
                )
        else:
            print("DEBUG: No class found → skills queryset empty")
            self.fields['skills'].queryset = Skill.objects.none()

        print("DEBUG: skills queryset =", list(self.fields['skills'].queryset))

# Tabela "Spells Known" dla klas, które mają sztywny limit (z PHB 5e)
# Format: 'Klasa': {Level: Liczba_Czarów}
SPELLS_KNOWN_TABLE = {
    'Bard': {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 14, 11: 15, 12: 15, 13: 16, 14: 18, 15: 19, 16: 19, 17: 20, 18: 22, 19: 22, 20: 22},
    'Sorcerer': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 12, 13: 13, 14: 13, 15: 14, 16: 14, 17: 15, 18: 15, 19: 15, 20: 15},
    'Warlock': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10, 11: 11, 12: 11, 13: 12, 14: 12, 15: 13, 16: 13, 17: 14, 18: 14, 19: 15, 20: 15},
    'Ranger': {1: 0, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8, 14: 8, 15: 9, 16: 9, 17: 10, 18: 10, 19: 11, 20: 11},
    # Paladin i inni Prepared Casters są liczeni wzorem, nie tabelą
}

CANTRIPS_KNOWN_TABLE = {
    'Bard': {1: 2, 4: 3, 10: 4},
    'Cleric': {1: 3, 4: 4, 10: 5},
    'Druid': {1: 2, 4: 3, 10: 4},
    'Sorcerer': {1: 4, 4: 5, 10: 6},
    'Warlock': {1: 2, 4: 3, 10: 4},
    'Wizard': {1: 3, 4: 4, 10: 5},
}

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
            # Pobieramy obiekt klasy i poziom postaci
            char_class = character.character_class
            char_level = character.level
            
            
            self.fields['spells'].queryset = Spell.objects.filter(
                classspell__character_class=char_class,
                classspell__unlock_level__lte=char_level
            ).order_by('level', 'name').distinct()
            self.fields['spells'].label = ""
    def clean(self):
        cleaned_data = super().clean()
        spells = cleaned_data.get('spells')
        character = self.instance
        
        if not spells or not character:
            return cleaned_data

        # --- Rozdzielamy Cantripy (lvl 0) i Spelle (lvl 1+) ---
        cantrips_selected = [s for s in spells if s.level == 0]
        leveled_spells_selected = [s for s in spells if s.level > 0]
        
        c_count = len(cantrips_selected)
        s_count = len(leveled_spells_selected)

        # Pobieramy dane postaci
        char_class = character.character_class.name
        level = character.level
        
        # --- 1. WALIDACJA CANTRIPÓW ---
        max_cantrips = 0
        if char_class in CANTRIPS_KNOWN_TABLE:
            # Szukamy odpowiedniego progu (np. jeśli level 5, bierzemy wartość dla level 4)
            table = CANTRIPS_KNOWN_TABLE[char_class]
            for lvl_threshold in sorted(table.keys()):
                if level >= lvl_threshold:
                    max_cantrips = table[lvl_threshold]
        
        # Jeśli klasa ma cantripy i wybrano za dużo
        if max_cantrips > 0 and c_count > max_cantrips:
            self.add_error('spells', f"Too many Cantrips selected! You can have max {max_cantrips}, but you selected {c_count}.")

        # --- 2. WALIDACJA CZARÓW POZIOMOWYCH (Level 1+) ---
        max_spells = 0
        limit_type = "Known" # Czy to "Znane" czy "Przygotowane"

        # A) Prepared Casters (Wzór: Level + Modifier)
        if char_class in ['Cleric', 'Druid', 'Wizard']:
            limit_type = "Prepared"
            # Pobierz modyfikator (Cleric/Druid -> Wis, Wizard -> Int)
            modifier = 0
            if char_class == 'Wizard':
                modifier = character.get_ability_modifier('intelligence')
            else:
                modifier = character.get_ability_modifier('wisdom')
            
            # Minimum 1 czar
            max_spells = max(1, level + modifier)
        
        elif char_class == 'Paladin':
            limit_type = "Prepared"
            modifier = character.get_ability_modifier('charisma')
            max_spells = max(1, (level // 2) + modifier)

        # B) Known Casters (Sztywna Tabela)
        elif char_class in SPELLS_KNOWN_TABLE:
            limit_type = "Known"
            max_spells = SPELLS_KNOWN_TABLE[char_class].get(level, 0)

        # Sprawdzenie limitu
        if max_spells > 0 and s_count > max_spells:
            self.add_error('spells', f"Too many Spells selected! As a lvl {level} {char_class}, you can have max {max_spells} Spells {limit_type}. You selected {s_count}.")
            
        return cleaned_data