
import json
from django.core.management.base import BaseCommand
from base.models import Spell, CharacterClass

class Command(BaseCommand):
    help = 'Imports spells from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing the spells.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found at: {json_file_path}'))
            return

        spellbook = data.get('spellbook', {})

        for level_str, spells_in_level in spellbook.items():
            try:
                level = int(level_str.split('_')[-1])
            except (ValueError, IndexError):
                self.stdout.write(self.style.WARNING(f'Could not parse level from "{level_str}". Skipping.'))
                continue

            for spell_data in spells_in_level:
                spell, created = Spell.objects.update_or_create(
                    name=spell_data['name'],
                    defaults={
                        'level': level,
                        'school': spell_data.get('school', ''),
                        'casting_time': spell_data.get('cast', ''),
                        'components': spell_data.get('comp', ''),
                        'duration': spell_data.get('dur', ''),
                        'range': spell_data.get('range', ''),
                        'desc': '', # 'desc' is a required field, but not in the json. Providing empty string.
                        # The following fields are not in the JSON, so they will use model defaults:
                        # higher_level, page, material, ritual, concentration
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created spell: {spell.name}'))
                else:
                    self.stdout.write(f'Updated spell: {spell.name}')

                # Handle CharacterClass relations
                class_names = spell_data.get('classes', [])
                for class_name in class_names:
                    class_obj, class_created = CharacterClass.objects.get_or_create(name=class_name)
                    spell.dnd_classes.add(class_obj) # Corrected to 'dnd_classes'
                    if class_created:
                        self.stdout.write(self.style.SUCCESS(f'-- Created class: {class_obj.name}'))

        self.stdout.write(self.style.SUCCESS('Spell import complete.'))
