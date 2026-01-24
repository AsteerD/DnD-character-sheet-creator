from django.db import migrations
import os
import json

def create_classes_subclasses_spells(apps, schema_editor):
    CharacterClass = apps.get_model('base', 'CharacterClass')
    Subclass = apps.get_model('base', 'Subclass')
    Spell = apps.get_model('base', 'Spell')
    ClassSpell = apps.get_model('base', 'ClassSpell')

    classes_and_subclasses = [
        ("Barbarian", ["Path of the Berserker", "Path of the Zeolot", "Path of Totem warrior"]),
        ("Bard", ["College of Lore", "College of Glamour", "College of Whispers"]),
        ("Cleric", ["Life Domain", "Tempest Domain", "War Domain"]),
        ("Druid", ["Circle of the Moon", "Circle of the Land", "Circle of Spores"]),
        ("Fighter", ["Champion", "Battle Master", "Samurai"]),
        ("Monk", ["Way of the Open Hand", "Way of Four Elements", "Way of Shadow"]),
        ("Paladin", ["Oath of Devotion", "Oath of Vengance", "Oath of the Acients"]),
        ("Ranger", ["Hunter", "Beast master", "Gloom Stalker"]),
        ("Rogue", ["Thief", "Assasin", "Inquisitive"]),
        ("Sorcerer", ["Draconic Bloodline", "Wild Magic", "Divine Soul"]),
        ("Warlock", ["The Fiend", "The Hexblade", "The Great Old One"]),
        ("Wizard", ["School of Evocation", "Necromancy", "Divination"]),
    ]
    for class_name, subclasses in classes_and_subclasses:
        char_class, _ = CharacterClass.objects.get_or_create(name=class_name)
        for subclass_name in subclasses:
            Subclass.objects.get_or_create(name=subclass_name, character_class=char_class)

    json_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'management', 'commands', 'spellsv2.json'
    )

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise Exception(f"spellsv2.json not found at {json_file_path}. This file is required for this migration.")

    spellbook = data.get('spellbook', {})

    for level_str, spells_in_level in spellbook.items():
        try:
            level = int(level_str.split('_')[-1])
        except (ValueError, IndexError):
            continue

        for spell_data in spells_in_level:
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
            }

            spell, _ = Spell.objects.update_or_create(
                name=spell_data['name'],
                defaults=defaults
            )

            class_info = spell_data.get('classes', {})
            for class_name, unlock_level in class_info.items():
                try:
                    class_obj = CharacterClass.objects.get(name=class_name)
                    ClassSpell.objects.get_or_create(
                        spell=spell,
                        character_class=class_obj,
                        defaults={'unlock_level': unlock_level}
                    )
                except CharacterClass.DoesNotExist:
                    # In case a class in the JSON is not in our predefined list
                    pass

def remove_classes_subclasses_spells(apps, schema_editor):
    CharacterClass = apps.get_model('base', 'CharacterClass')
    Subclass = apps.get_model('base', 'Subclass')
    Spell = apps.get_model('base', 'Spell')
    # Remove all subclasses, classes, and spells
    Subclass.objects.all().delete()
    CharacterClass.objects.all().delete()
    Spell.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_characterclass_remove_character_subclass_and_more"),
    ]
    operations = [
        migrations.RunPython(create_classes_subclasses_spells, remove_classes_subclasses_spells),
     
    ]
