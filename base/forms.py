from django import forms
from .models import Character, Skill, Subclass, CharacterClass, Spell, Feat
from django.core.exceptions import ValidationError

class CharacterForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Class Skill Proficiencies"
    )
    feats = forms.ModelMultipleChoiceField(
        queryset=Feat.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Feats"
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
            'feats',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("DEBUG: Initializing CharacterForm")

        # Subclasses logic
        if self.instance.pk and self.instance.character_class:
            self.fields['subclass'].queryset = Subclass.objects.filter(
                character_class=self.instance.character_class
            )
        elif 'character_class' in self.data:
            try:
                class_id = int(self.data.get('character_class'))
                self.fields['subclass'].queryset = Subclass.objects.filter(
                    character_class_id=class_id
                )
            except (ValueError, TypeError):
                self.fields['subclass'].queryset = Subclass.objects.none()
        else:
            self.fields['subclass'].queryset = Subclass.objects.all()

        # Skills logic
        char_class = None
        if self.instance.pk and self.instance.character_class:
            char_class = self.instance.character_class
        elif 'character_class' in self.data:
            try:
                class_id = int(self.data.get('character_class'))
                char_class = CharacterClass.objects.get(pk=class_id)
            except (ValueError, TypeError, CharacterClass.DoesNotExist):
                char_class = None
        else:
            char_class = CharacterClass.objects.first()

        if char_class:
            self.fields['skills'].queryset = Skill.objects.filter(
                classskillchoice__character_class=char_class
            )
            if self.instance.pk:
                self.fields['skills'].initial = (
                    self.instance.characterskillproficiency_set.values_list('skill_id', flat=True)
                )
        else:
            self.fields['skills'].queryset = Skill.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        feats = cleaned_data.get('feats')
        level = cleaned_data.get('level')
        
        if level is None:
            if self.instance and self.instance.pk:
                level = self.instance.level
            else:
                level = 1 
        
        try:
            level = int(level)
        except (ValueError, TypeError):
            level = 1

        max_feats = level // 4
        selected_count = len(feats) if feats else 0

        if feats and selected_count > max_feats:
            error_msg = f"Too many Feats! At level {level}, you can have max {max_feats} feats."
            self.add_error('feats', error_msg)
            
        return cleaned_data


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

        cantrips_selected = [s for s in spells if s.level == 0]
        leveled_spells_selected = [s for s in spells if s.level > 0]
        
        c_count = len(cantrips_selected)
        s_count = len(leveled_spells_selected)

        max_cantrips = character.max_cantrips_known 
        if max_cantrips > 0 and c_count > max_cantrips:
            self.add_error('spells', f"Too many Cantrips selected! You can have max {max_cantrips}, but you selected {c_count}.")

        max_spells, limit_type = character.max_spells_known
        if max_spells > 0 and s_count > max_spells:
            self.add_error(
                'spells', 
                f"Too many Spells selected! As a lvl {character.level} {character.character_class.name}, "
                f"you can have max {max_spells} Spells {limit_type}. You selected {s_count}."
            )
            
        return cleaned_data