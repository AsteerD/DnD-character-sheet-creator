from django.db import migrations
import os
import json

def create_classes_subclasses_spells(apps, schema_editor):
    CharacterClass = apps.get_model('base', 'CharacterClass')
    Subclass = apps.get_model('base', 'Subclass')
    Spell = apps.get_model('base', 'Spell')

    classes_and_subclasses = [
        ("Barbarian", ["Path of the Berserker", "Path of the Zeolot", "Path of Totem warrior"]),
        ("Bard", ["College of Lore", "College of Glamour", "College of Whispers"]),
        ("Cleric", ["Life Domain", "Tempest Domain", "War Domain"]),
        ("Druid", ["Circle of the Moon", "Circle of the Land", "Circle of Spores"]),
        ("Fighter", ["Champion", "Battle Master", "Eldritch Knight"]),
        ("Monk", ["Way of the Open Hand", "Way of Four Elements", "Way of Shadow"]),
        ("Paladin", ["Oath of Devotion", "Oath of Vengance", "Oath of the Acients"]),
        ("Ranger", ["Hunter", "Beast master", "Gloom Stalker"]),
        ("Rogue", ["Thief", "Assasin", "Arcane Trickster"]),
        ("Sorcerer", ["Draconic Bloodline", "Wild Magic", "Divine Soul"]),
        ("Warlock", ["The Fiend", "The Hexblade", "The Great Old One"]),
        ("Wizard", ["School of Evocation", "Necromancy", "Divination"]),
    ]
    class_objs = {}
    for class_name, subclasses in classes_and_subclasses:
        char_class, _ = CharacterClass.objects.get_or_create(name=class_name)
        class_objs[class_name] = char_class
        for subclass_name in subclasses:
            Subclass.objects.get_or_create(name=subclass_name, character_class=char_class)

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spells_path = os.path.join(base_dir, 'spellsv2.json')
    if not os.path.exists(spells_path):
        return  # skip if not found
    with open(spells_path, encoding='utf-8') as f:
        spells = json.load(f)
    for spell in spells:
        Spell.objects.get_or_create(
            name=spell['name'],
            defaults={
                'desc': spell.get('desc', ''),
                'range': spell.get('range', ''),
                'components': spell.get('components', ''),
                'material': spell.get('material', ''),
                'ritual': spell.get('ritual', False),
                'duration': spell.get('duration', ''),
                'concentration': spell.get('concentration', False),
                'casting_time': spell.get('casting_time', ''),
                'level': spell.get('level', 0),
                'school': spell.get('school', ''),
            }
        )

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
