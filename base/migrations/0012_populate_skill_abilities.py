from django.db import migrations

SKILL_ABILITIES = {
    "Acrobatics": "dexterity",
    "Animal Handling": "wisdom",
    "Arcana": "intelligence",
    "Athletics": "strength",
    "Deception": "charisma",
    "History": "intelligence",
    "Insight": "wisdom",
    "Intimidation": "charisma",
    "Investigation": "intelligence",
    "Medicine": "wisdom",
    "Nature": "intelligence",
    "Perception": "wisdom",
    "Performance": "charisma",
    "Persuasion": "charisma",
    "Religion": "intelligence",
    "Sleight of Hand": "dexterity",
    "Stealth": "dexterity",
    "Survival": "wisdom",
}



def populate_skill_abilities(apps, schema_editor):
    Skill = apps.get_model("base", "Skill")

    for skill_name, ability in SKILL_ABILITIES.items():
        Skill.objects.filter(name=skill_name).update(ability=ability)


def populate_class_skill_choices(apps, schema_editor):
    CharacterClass = apps.get_model("base", "CharacterClass")
    Skill = apps.get_model("base", "Skill")
    ClassSkillChoice = apps.get_model("base", "ClassSkillChoice")

    data = {
        "Barbarian": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
        "Bard": ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"],
        "Cleric": ["History", "Insight", "Medicine", "Persuasion", "Religion"],
        "Druid": ["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
        "Fighter": ["Athletics", "Acrobatics", "Perception", "Survival", "Intimidation", "History"],
        "Monk": ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"],
        "Paladin": ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"],
        "Ranger": ["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
        "Rogue": ["Stealth", "Acrobatics", "Sleight of Hand", "Perception", "Deception", "Investigation"],
        "Sorcerer": ["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"],
        "Warlock": ["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"],
        "Wizard": ["Arcana", "History", "Investigation", "Religion"],
    }

    for class_name, skills in data.items():
        char_class = CharacterClass.objects.get(name=class_name)
        for skill_name in skills:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            ClassSkillChoice.objects.get_or_create(
                character_class=char_class,
                skill=skill
            )

class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_characterclass_skill_choices_count_skill_ability_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_skill_abilities),
        migrations.RunPython(populate_class_skill_choices),
    ]