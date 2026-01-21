from django import forms
from .models import Character, SubclassChoices


class CharacterForm(forms.ModelForm):

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
            'armor_class',
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
        
        widgets = {
            'backstory': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'inspiration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['inspiration']: 
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        char_class = cleaned_data.get('character_class')
        subclass = cleaned_data.get('subclass')

        allowed_subclasses = {
            'ROGUE': ['thief', 'assassin', 'trickster'],
            'CLERIC': ['life', 'war', 'light'],
            'FIGHTER': ['champion', 'battle_master', 'eldritch_knight'],
            'PALADIN': ['devotion', 'ancients', 'vengeance'],
            'RANGER': ['hunter', 'beast_master', 'gloom_stalker'],
            'BARD': ['lore', 'valor', 'glamour'],
        }

        if char_class in allowed_subclasses:
            if subclass and subclass != 'none' and subclass not in allowed_subclasses[char_class]:
                raise forms.ValidationError(f"Invalid subclass for {char_class}")
        return cleaned_data