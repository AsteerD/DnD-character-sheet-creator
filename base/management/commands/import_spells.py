import json
from django.core.management.base import BaseCommand
from base.models import Spell, CharacterClass
import os

class Command(BaseCommand):
    help = 'Imports spells from a JSON file into the database.'

    def handle(self, *args, **options):
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'spells.json')

        with open(json_file_path) as f:
            data = json.load(f)
        
        spellbook = data['spellbook']

        school_map = {
            "Abj": "Abjuration", "Conj": "Conjuration", "Div": "Divination",
            "Ench": "Enchantment", "Evo": "Evocation", "Ill": "Illusion",
            "Necro": "Necromancy", "Trans": "Transmutation"
        }

        for level_str, spells in spellbook.items():
            level = int(level_str.split('_')[-1])
            for spell_data in spells:
                spell_name = spell_data['name']
                # Skip spells with placeholder names
                if 'x' in spell_name.lower():
                    self.stdout.write(self.style.WARNING(f'Skipping spell with placeholder name: {spell_name}'))
                    continue

                spell, created = Spell.objects.get_or_create(
                    name=spell_name,
                    defaults={
                        'level': level,
                        'school': school_map.get(spell_data['school'], spell_data['school']),
                        'cast_time': spell_data['cast'],
                        'components': spell_data['comp'],
                        'duration': spell_data['dur'],
                        'range_area': spell_data['range'],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created spell: {spell.name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Spell already exists: {spell.name}, updating classes...'))
                    spell.level = level
                    spell.school = school_map.get(spell_data['school'], spell_data['school'])
                    spell.cast_time = spell_data['cast']
                    spell.components = spell_data['comp']
                    spell.duration = spell_data['dur']
                    spell.range_area = spell_data['range']
                    spell.save()


                spell.available_to_classes.clear()
                for class_name in spell_data['classes']:
                    char_class, _ = CharacterClass.objects.get_or_create(name=class_name)
                    spell.available_to_classes.add(char_class)

        self.stdout.write(self.style.SUCCESS('Successfully imported all spells.'))
