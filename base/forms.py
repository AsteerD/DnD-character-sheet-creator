# base/forms.py
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
        widget=forms.CheckboxSelectMultiple,  # <--- TO MUSI TU BYĆ
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

        # Filter the spells displayed in the form based on class and level
        if character and character.pk:
            char_class = character.character_class
            char_level = character.level
            
            self.fields['spells'].queryset = Spell.objects.filter(
                classspell__character_class=char_class,
                classspell__unlock_level__lte=char_level
            ).order_by('level', 'name').distinct()
            
            self.fields['spells'].label = ""

    def clean(self):
        super().clean()
        self.validate_feats()

    def validate_feats(self):

        feats = self.cleaned_data.get('feats')
        level = self.cleaned_data.get('level')
        
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

        print(f"DEBUG: Checking Feats. Level: {level}, Max: {max_feats}, Selected: {selected_count}")

        if feats and selected_count > max_feats:
            self.add_error('feats', f"Too many Feats! At level {level}, you can have max {max_feats} feats.")