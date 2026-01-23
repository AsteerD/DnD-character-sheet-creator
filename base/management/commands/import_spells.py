import json
from django.core.management.base import BaseCommand
from base.models import Spell, CharacterClass, ClassSpell

class Command(BaseCommand):
    help = 'Imports spells from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing the spells.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
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
                # Defaults for fields that might be missing in the JSON
                defaults = {
                    'level': level,
                    'school': spell_data.get('school', ''),
                    'casting_time': spell_data.get('cast', ''),
                    'components': spell_data.get('comp', ''),
                    'duration': spell_data.get('dur', ''),
                    'range': spell_data.get('range', ''),
                    'desc': spell_data.get('desc', 'No description available.'),
                    'material': spell_data.get('material', ''),
                    'ritual': spell_data.get('ritual', False),
                    'concentration': 'concentration' in spell_data.get('dur', '').lower(),
                    'page': spell_data.get('page', 'N/A'),
                    'higher_level': spell_data.get('higher_level', None),
                }

                spell, created = Spell.objects.update_or_create(
                    name=spell_data['name'],
                    defaults=defaults
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created spell: {spell.name}'))
                else:
                    self.stdout.write(f'Updated spell: {spell.name}')

                # Handle CharacterClass and ClassSpell relations
                class_info = spell_data.get('classes', {})
                for class_name, unlock_level in class_info.items():
                    class_obj, class_created = CharacterClass.objects.get_or_create(name=class_name)
                    if class_created:
                        self.stdout.write(self.style.SUCCESS(f'-- Created class: {class_obj.name}'))

                    # Create or update the through model instance
                    class_spell, through_created = ClassSpell.objects.get_or_create(
                        spell=spell,
                        character_class=class_obj,
                        defaults={'unlock_level': unlock_level}
                    )
                    
                    if through_created:
                        self.stdout.write(f'-- Associated {spell.name} with {class_obj.name} at level {unlock_level}')
                    else:
                        # If you want to update the unlock_level if it changes
                        if class_spell.unlock_level != unlock_level:
                            class_spell.unlock_level = unlock_level
                            class_spell.save()
                            self.stdout.write(f'-- Updated {spell.name} for {class_obj.name} to level {unlock_level}')

        self.stdout.write(self.style.SUCCESS('Spell import complete.'))
