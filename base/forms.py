# base/forms.py
from django import forms
from .models import Character, Skill, Subclass, CharacterClass

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
            'initiative',
            'speed',
            'hit_points',
            'temporary_hit_points',
            'hit_dice',
            'death_saves_success',
            'death_saves_failure',
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
