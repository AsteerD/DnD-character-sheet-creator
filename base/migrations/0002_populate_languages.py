from django.db import migrations


def create_languages(apps, schema_editor):
    Language = apps.get_model('base', 'Language')
    languages = [
        "Common",
        "Common Sign Language",
        "Dwarvish",
        "Elvish",
        "Giant",
        "Gnomish",
        "Goblin",
        "Halfling",
        "Orc",
        "Abyssal",
        "Celestial",
        "Draconic",
        "Druidic",
        "Deep Speech",
        "Infernal",
        "Primordial",
        "Sylvan",
        "Thieves’ Cant",
        "Undercommon",
    ]
    for name in languages:
        Language.objects.get_or_create(name=name)


def remove_languages(apps, schema_editor):
    Language = apps.get_model('base', 'Language')
    names = [
        "Common",
        "Common Sign Language"
        "Dwarvish",
        "Elvish",
        "Giant",
        "Gnomish",
        "Goblin",
        "Halfling",
        "Orc",
        "Abyssal",
        "Celestial",
        "Draconic",
        "Druidic",
        "Deep Speech",
        "Infernal",
        "Primordial",
        "Sylvan",
        "Thieves’ Cant",
        "Undercommon",
    ]
    Language.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_languages, remove_languages),
    ]
