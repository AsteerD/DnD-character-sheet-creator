from django import forms
from django.core.exceptions import ValidationError
from .models import Character, CharacterClass, Subclass, Feat, Language

class CharacterForm(forms.ModelForm):
    character_class = forms.ModelChoiceField(
        queryset=CharacterClass.objects.all(),
        label="Class",
        empty_label="Select Class"
    )

    feats = forms.ModelMultipleChoiceField(
        queryset=Feat.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Feats (Optional)"
    )

    # Dodajemy też ładne widgety dla języków, skoro to teraz ManyToMany
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Languages"
    )

    class Meta:
        model = Character
        # USUNĄŁEM 'armor_class' z tej listy poniżej
        fields = [
            'character_name', 'race', 
            'character_class', 
            'subclass', 
            'level', 
            'feats',
            'background', 'alignment', 'backstory',
            'strength', 'dexterity', 'constitution', 
            'intelligence', 'wisdom', 'charisma',
            'hit_points', 'speed', 'initiative', 'hit_dice',
            'inspiration', 'languages',
            'experience_points', 
            'death_saves_success', 'death_saves_failure'
        ]
        widgets = {
            'backstory': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subclass'].queryset = Subclass.objects.none()

        if 'character_class' in self.data:
            try:
                class_id = int(self.data.get('character_class'))
                self.fields['subclass'].queryset = Subclass.objects.filter(character_class_id=class_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.character_class:
            self.fields['subclass'].queryset = self.instance.character_class.subclasses.all()

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        feats = cleaned_data.get('feats')
        character_class = cleaned_data.get('character_class')

        if level and feats:
            allowed_feats = 0
            feat_levels = [4, 8, 12, 16, 19]

            if character_class:
                if character_class.name == "Fighter":
                    feat_levels.extend([6, 14])
                elif character_class.name == "Rogue":
                    feat_levels.append(10)

            for lvl_threshold in feat_levels:
                if level >= lvl_threshold:
                    allowed_feats += 1

            if len(feats) > allowed_feats:
                raise ValidationError(
                    f"At level {level}, you can select a maximum of {allowed_feats} feats. You selected {len(feats)}."
                )

        return cleaned_data