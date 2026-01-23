from django.db import migrations
from decimal import Decimal

def create_starting_equipment(apps, schema_editor):
    CharacterClass = apps.get_model("base", "CharacterClass")
    Item = apps.get_model("base", "Item")
    StartingEquipment = apps.get_model("base", "StartingEquipment")

    # PHB item definitions: name → (weight, value_gp)
    ITEM_STATS = {
        "Greataxe": (Decimal("7"), 30),
        "Handaxe": (Decimal("2"), 5),
        "Explorer's Pack": (Decimal("59"), 10),
        "Javelin": (Decimal("2"), Decimal("0.5")),

        "Rapier": (Decimal("2"), 25),
        "Shortbow": (Decimal("2"), 25),
        "Diplomat's Pack": (Decimal("39"), 39),
        "Lute": (Decimal("2"), 35),
        "Leather Armor": (Decimal("10"), 10),
        "Dagger": (Decimal("1"), 2),

        "Mace": (Decimal("4"), 5),
        "Scale Mail": (Decimal("45"), 50),
        "Light Crossbow": (Decimal("5"), 25),
        "Crossbow Bolt": (Decimal("1.5"), 1),  # 20 bolts
        "Priest's Pack": (Decimal("24"), 19),
        "Shield": (Decimal("6"), 10),
        "Holy Symbol": (Decimal("1"), 5),

        "Quarterstaff": (Decimal("4"), Decimal("0.2")),
        "Druidic Focus": (Decimal("1"), 5),

        "Chain Mail": (Decimal("55"), 75),
        "Longsword": (Decimal("3"), 15),
        "Dungeoneer's Pack": (Decimal("61"), 12),

        "Shortsword": (Decimal("2"), 10),
        "Dart": (Decimal("0.25"), Decimal("0.05")),

        "Martial Weapon": (Decimal("3"), 15),  # abstract placeholder
        "Simple Weapon": (Decimal("3"), 1),    # abstract placeholder

        "Longbow": (Decimal("2"), 50),
        "Arrow": (Decimal("1"), 1),  # 20 arrows

        "Burglar's Pack": (Decimal("47.5"), 16),
        "Thieves' Tools": (Decimal("1"), 25),

        "Scholar's Pack": (Decimal("10"), 40),
        "Spellbook": (Decimal("3"), 50),
        "Arcane Focus": (Decimal("1"), 10),
    }

    equipment_data = [
        ("Barbarian", "Greataxe", 1),
        ("Barbarian", "Handaxe", 2),
        ("Barbarian", "Explorer's Pack", 1),
        ("Barbarian", "Javelin", 4),

        ("Bard", "Rapier", 1),
        ("Bard", "Diplomat's Pack", 1),
        ("Bard", "Lute", 1),
        ("Bard", "Leather Armor", 1),
        ("Bard", "Dagger", 1),

        ("Cleric", "Mace", 1),
        ("Cleric", "Scale Mail", 1),
        ("Cleric", "Light Crossbow", 1),
        ("Cleric", "Crossbow Bolt", 20),
        ("Cleric", "Priest's Pack", 1),
        ("Cleric", "Shield", 1),
        ("Cleric", "Holy Symbol", 1),

        ("Druid", "Quarterstaff", 1),
        ("Druid", "Leather Armor", 1),
        ("Druid", "Explorer's Pack", 1),
        ("Druid", "Druidic Focus", 1),

        ("Fighter", "Chain Mail", 1),
        ("Fighter", "Longsword", 1),
        ("Fighter", "Shield", 1),
        ("Fighter", "Light Crossbow", 1),
        ("Fighter", "Crossbow Bolt", 20),
        ("Fighter", "Dungeoneer's Pack", 1),

        ("Monk", "Shortsword", 1),
        ("Monk", "Dungeoneer's Pack", 1),
        ("Monk", "Dart", 10),

        ("Paladin", "Chain Mail", 1),
        ("Paladin", "Martial Weapon", 1),
        ("Paladin", "Shield", 1),
        ("Paladin", "Javelin", 5),
        ("Paladin", "Priest's Pack", 1),
        ("Paladin", "Holy Symbol", 1),

        ("Ranger", "Scale Mail", 1),
        ("Ranger", "Shortsword", 2),
        ("Ranger", "Dungeoneer's Pack", 1),
        ("Ranger", "Longbow", 1),
        ("Ranger", "Arrow", 20),

        ("Rogue", "Rapier", 1),
        ("Rogue", "Shortbow", 1),
        ("Rogue", "Arrow", 20),
        ("Rogue", "Burglar's Pack", 1),
        ("Rogue", "Leather Armor", 1),
        ("Rogue", "Dagger", 2),
        ("Rogue", "Thieves' Tools", 1),

        ("Sorcerer", "Dagger", 2),
        ("Sorcerer", "Light Crossbow", 1),
        ("Sorcerer", "Crossbow Bolt", 20),
        ("Sorcerer", "Explorer's Pack", 1),
        ("Sorcerer", "Arcane Focus", 1),

        ("Warlock", "Light Crossbow", 1),
        ("Warlock", "Crossbow Bolt", 20),
        ("Warlock", "Leather Armor", 1),
        ("Warlock", "Simple Weapon", 1),
        ("Warlock", "Scholar's Pack", 1),
        ("Warlock", "Arcane Focus", 1),

        ("Wizard", "Quarterstaff", 1),
        ("Wizard", "Dagger", 1),
        ("Wizard", "Scholar's Pack", 1),
        ("Wizard", "Spellbook", 1),
        ("Wizard", "Arcane Focus", 1),
    ]

    for class_name, item_name, quantity in equipment_data:
        char_class = CharacterClass.objects.get(name=class_name)
        weight, value = ITEM_STATS[item_name]

        item, _ = Item.objects.get_or_create(
            name=item_name,
            defaults={"weight": weight, "value": value},
        )

        StartingEquipment.objects.update_or_create(
            character_class=char_class,
            item=item,
            defaults={"quantity": quantity},
        )

def remove_starting_equipment(apps, schema_editor):
    apps.get_model("base", "StartingEquipment").objects.all().delete()
    apps.get_model("base", "Item").objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ("base", "0007_startingequipment"),
    ]

    operations = [
        migrations.RunPython(create_starting_equipment, remove_starting_equipment),
    ]
