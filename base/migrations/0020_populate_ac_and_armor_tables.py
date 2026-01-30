from django.db import migrations

def populate_ac_core(apps, schema_editor):
    CharacterClass = apps.get_model("base", "CharacterClass")
    Subclass = apps.get_model("base", "Subclass")
    Item = apps.get_model("base", "Item")

    Armor = apps.get_model("base", "Armor")
    Shield = apps.get_model("base", "Shield")
    ArmorClassFormula = apps.get_model("base", "ArmorClassFormula")
    ArmorClassBonus = apps.get_model("base", "ArmorClassBonus")

    # =================================================
    # ARMOR DEFINITIONS (PHB)
    # =================================================

    ARMOR_DATA = [
        ("Leather Armor", "light", 11, True, None, None),
        ("Scale Mail", "medium", 14, True, 2, None),
        ("Chain Mail", "heavy", 16, False, None, 13),
    ]

    for name, armor_type, base, adds_dex, cap, str_req in ARMOR_DATA:
        item = Item.objects.filter(name=name).first()
        if not item:
            continue

        Armor.objects.get_or_create(
            item=item,
            defaults={
                "armor_type": armor_type,
                "base_ac": base,
                "adds_dex": adds_dex,
                "max_dex_bonus": cap,
                "str_requirement": str_req
            }
        )

    # =================================================
    # SHIELD
    # =================================================

    shield_item = Item.objects.filter(name="Shield").first()
    if shield_item:
        Shield.objects.get_or_create(
            item=shield_item,
            defaults={"ac_bonus": 2}
        )

    # =================================================
    # PASSIVE AC FORMULAS
    # =================================================
    # class_name, subclass_name, base, dex, wis, con, int

    CLASS_FORMULAS = [
        ("Barbarian", None, 10, True, False, True, False),
        ("Monk", None, 10, True, True, False, False),
        ("Sorcerer", "Draconic Bloodline", 13, True, False, False, False),
    ]

    for cls_name, sub_name, base, dex, wis, con, inte in CLASS_FORMULAS:
        cls = CharacterClass.objects.filter(name=cls_name).first()
        if not cls:
            continue

        subclass = None
        if sub_name:
            subclass = Subclass.objects.filter(
                name=sub_name,
                character_class=cls
            ).first()

        ArmorClassFormula.objects.get_or_create(
            character_class=cls,
            subclass=subclass,
            min_level=1,
            defaults={
                "base": base,
                "use_dex": dex,
                "use_wis": wis,
                "use_con": con,
                "use_int": inte,
            }
        )

    # =================================================
    # PASSIVE FLAT BONUSES
    # =================================================
    # class_name, subclass_name, bonus

    CLASS_BONUSES = [
        ("Cleric", "Forge", 1),
    ]

    for cls_name, sub_name, bonus in CLASS_BONUSES:
        cls = CharacterClass.objects.filter(name=cls_name).first()
        if not cls:
            continue

        subclass = Subclass.objects.filter(
            name=sub_name,
            character_class=cls
        ).first()

        if not subclass:
            continue

        ArmorClassBonus.objects.get_or_create(
            character_class=cls,
            subclass=subclass,
            min_level=1,
            defaults={"flat_bonus": bonus}
        )


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0019_armor_armorclassbonus_armorclassformula_shield_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_ac_core),
    ]
