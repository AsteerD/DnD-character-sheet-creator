from django.db import migrations

def populate_features(apps, schema_editor):
    CharacterClass = apps.get_model('base', 'CharacterClass')
    ClassFeature = apps.get_model('base', 'ClassFeature')
    Feat = apps.get_model('base', 'Feat')

    # --- 1. POPULATE FEATS (Przykładowe z SRD) ---
    feats_data = [
        ("Grappler", "You have advantage on attack rolls against a creature you are grappling...", "Str 13"),
        ("Healer", "When you use a healer's kit to stabilize a dying creature, that creature also regains 1 hit point...", None),
        ("Lucky", "You have 3 luck points...", None),
        ("Sentinel", "When you hit a creature with an opportunity attack, the creature's speed becomes 0...", None),
        ("Sharpshooter", "Attacking at long range doesn't impose disadvantage...", None),
        ("War Caster", "You have advantage on Constitution saving throws that you make to maintain your concentration...", "Spellcasting"),
        ("Great Weapon Master", "On your turn, when you score a critical hit with a melee weapon...", None),
    ]

    for name, desc, prereq in feats_data:
        Feat.objects.get_or_create(name=name, defaults={"description": desc, "prerequisite": prereq})

    # --- 2. POPULATE CLASS FEATURES ---
    # Struktura: (Nazwa Klasy, Level, Nazwa Cechy, Opis)
    # Dodajemy kluczowe cechy z SRD dla poziomów 1-20
    
    features_data = [
        # --- BARBARIAN ---
        ("Barbarian", 1, "Rage", "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action."),
        ("Barbarian", 1, "Unarmored Defense", "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier."),
        ("Barbarian", 2, "Reckless Attack", "You can throw aside all concern for defense to attack with fierce desperation."),
        ("Barbarian", 2, "Danger Sense", "You have advantage on Dexterity saving throws against effects that you can see."),
        ("Barbarian", 5, "Extra Attack", "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
        ("Barbarian", 5, "Fast Movement", "Your speed increases by 10 feet while you aren't wearing heavy armor."),
        ("Barbarian", 7, "Feral Instinct", "Your instincts are so honed that you have advantage on initiative rolls."),
        ("Barbarian", 11, "Relentless Rage", "Your rage can keep you fighting despite grievous wounds."),
        ("Barbarian", 15, "Persistent Rage", "Your rage is so fierce that it ends early only if you fall unconscious or if you choose to end it."),
        ("Barbarian", 20, "Primal Champion", "Your Strength and Constitution scores increase by 4."),

        # --- BARD ---
        ("Bard", 1, "Spellcasting", "You have learned to untangle and reshape the fabric of reality in harmony with your wishes and music."),
        ("Bard", 1, "Bardic Inspiration", "You can inspire others through stirring words or music."),
        ("Bard", 2, "Jack of All Trades", "You can add half your proficiency bonus, rounded down, to any ability check you make that doesn't already include your proficiency bonus."),
        ("Bard", 2, "Song of Rest", "You can use soothing music or oration to help revitalize your wounded allies during a short rest."),
        ("Bard", 3, "Expertise", "Choose two of your skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."),
        ("Bard", 5, "Font of Inspiration", "You regain all of your expended uses of Bardic Inspiration when you finish a short or long rest."),
        ("Bard", 6, "Countercharm", "You gain the ability to use musical notes or words of power to disrupt mind-influencing effects."),
        ("Bard", 20, "Superior Inspiration", "When you roll initiative and have no uses of Bardic Inspiration left, you regain one use."),

        # --- CLERIC ---
        ("Cleric", 1, "Spellcasting", "As a conduit for divine power, you can cast cleric spells."),
        ("Cleric", 1, "Divine Domain", "Choose one domain related to your deity."),
        ("Cleric", 2, "Channel Divinity", "At 2nd level, you gain the ability to channel divine energy directly from your deity."),
        ("Cleric", 5, "Destroy Undead", "When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its Challenge Rating is at or below a certain threshold."),
        ("Cleric", 10, "Divine Intervention", "You can call on your deity to intervene on your behalf when your need is great."),

        # --- DRUID ---
        ("Druid", 1, "Druidic", "You know Druidic, the secret language of druids."),
        ("Druid", 1, "Spellcasting", "Drawing on the divine essence of nature itself, you can cast spells to shape that essence to your will."),
        ("Druid", 2, "Wild Shape", "You can use your action to magically assume the shape of a beast that you have seen before."),
        ("Druid", 18, "Timeless Body", "The primal magic that you wield causes you to age more slowly. For every 10 years that pass, your body ages only 1 year."),
        ("Druid", 20, "Archdruid", "You can use your Wild Shape an unlimited number of times."),

        # --- FIGHTER ---
        ("Fighter", 1, "Fighting Style", "You adopt a particular style of fighting as your specialty."),
        ("Fighter", 1, "Second Wind", "You have a limited well of stamina that you can draw on to protect yourself from harm."),
        ("Fighter", 2, "Action Surge", "You can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action."),
        ("Fighter", 5, "Extra Attack", "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
        ("Fighter", 9, "Indomitable", "You can reroll a saving throw that you fail."),
        ("Fighter", 11, "Extra Attack (2)", "You can attack three times, instead of once, whenever you take the Attack action on your turn."),
        ("Fighter", 20, "Extra Attack (3)", "You can attack four times, instead of once, whenever you take the Attack action on your turn."),

        # --- MONK ---
        ("Monk", 1, "Unarmored Defense", "While you are wearing no armor and not wielding a shield, your AC equals 10 + your Dex modifier + your Wis modifier."),
        ("Monk", 1, "Martial Arts", "Your practice of martial arts gives you mastery of combat styles that use unarmed strikes and monk weapons."),
        ("Monk", 2, "Ki", "Your training allows you to harness the mystic energy of ki."),
        ("Monk", 2, "Unarmored Movement", "Your speed increases by 10 feet while you are not wearing armor or wielding a shield."),
        ("Monk", 3, "Deflect Missiles", "You can use your reaction to deflect or catch the missile when you are hit by a ranged weapon attack."),
        ("Monk", 5, "Extra Attack", "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
        ("Monk", 5, "Stunning Strike", "You can interfere with the flow of ki in an opponent's body."),
        ("Monk", 7, "Evasion", "When you are subjected to an effect that allows you to make a Dex saving throw to take only half damage, you instead take no damage if you succeed."),
        ("Monk", 20, "Perfect Self", "At 20th level, when you roll for initiative and have no ki points remaining, you regain 4 ki points."),

        # --- PALADIN ---
        ("Paladin", 1, "Divine Sense", "The presence of strong evil registers on your senses like a noxious odor."),
        ("Paladin", 1, "Lay on Hands", "Your blessed touch can heal wounds."),
        ("Paladin", 2, "Fighting Style", "You adopt a particular style of fighting as your specialty."),
        ("Paladin", 2, "Spellcasting", "By 2nd level, you have learned to draw on divine magic."),
        ("Paladin", 2, "Divine Smite", "When you hit a creature with a melee weapon attack, you can expend one spell slot to deal radiant damage."),
        ("Paladin", 3, "Divine Health", "You are immune to disease."),
        ("Paladin", 5, "Extra Attack", "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
        ("Paladin", 6, "Aura of Protection", "Whenever you or a friendly creature within 10 feet of you must make a saving throw, the creature gains a bonus equal to your Charisma modifier."),

        # --- RANGER ---
        ("Ranger", 1, "Favored Enemy", "You have significant experience studying, tracking, hunting, and even talking to a certain type of enemy."),
        ("Ranger", 1, "Natural Explorer", "You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions."),
        ("Ranger", 2, "Fighting Style", "You adopt a particular style of fighting as your specialty."),
        ("Ranger", 2, "Spellcasting", "By 2nd level, you have learned to use the magical essence of nature to cast spells."),
        ("Ranger", 5, "Extra Attack", "You can attack twice, instead of once, whenever you take the Attack action on your turn."),
        ("Ranger", 14, "Vanish", "You can use the Hide action as a bonus action on your turn."),
        ("Ranger", 18, "Feral Senses", "You gain preternatural senses that help you fight creatures you can't see."),

        # --- ROGUE ---
        ("Rogue", 1, "Expertise", "Choose two of your skill proficiencies..."),
        ("Rogue", 1, "Sneak Attack", "Once per turn, you can deal extra 1d6 damage to one creature you hit with an attack if you have advantage on the attack roll."),
        ("Rogue", 1, "Thieves' Cant", "During your rogue training you learned thieves' cant, a secret mix of dialect, jargon, and code."),
        ("Rogue", 2, "Cunning Action", "You can take a bonus action on each of your turns in combat to Dash, Disengage, or Hide."),
        ("Rogue", 5, "Uncanny Dodge", "When an attacker that you can see hits you with an attack, you can use your reaction to halve the attack's damage."),
        ("Rogue", 7, "Evasion", "When you are subjected to an effect that allows you to make a Dex saving throw to take only half damage, you instead take no damage if you succeed."),
        ("Rogue", 11, "Reliable Talent", "Whenever you make an ability check that lets you add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10."),
        ("Rogue", 20, "Stroke of Luck", "If you miss with an attack roll, you can treat the roll as a 20."),

        # --- SORCERER ---
        ("Sorcerer", 1, "Spellcasting", "An event in your past, or in the life of a parent or ancestor, left an indelible mark on you, infusing you with arcane magic."),
        ("Sorcerer", 1, "Sorcerous Origin", "Choose a sorcerous origin, which describes the source of your innate magical power."),
        ("Sorcerer", 2, "Font of Magic", "You tap into a deep wellspring of magic within yourself. This wellspring is represented by sorcery points."),
        ("Sorcerer", 3, "Metamagic", "You gain the ability to twist your spells to suit your needs."),
        ("Sorcerer", 20, "Sorcerous Restoration", "You regain 4 expended sorcery points whenever you finish a short rest."),

        # --- WARLOCK ---
        ("Warlock", 1, "Otherworldly Patron", "At 1st level, you have struck a bargain with an otherworldly being of your choice."),
        ("Warlock", 1, "Pact Magic", "Your arcane research and the magic bestowed on you by your patron have given you facility with spells."),
        ("Warlock", 2, "Eldritch Invocations", "In your study of occult lore, you have unearthed eldritch invocations, fragments of forbidden knowledge."),
        ("Warlock", 3, "Pact Boon", "Your patron bestows a gift upon you for your loyal service."),
        ("Warlock", 11, "Mystic Arcanum", "Your patron bestows upon you a magical secret called an arcanum."),
        ("Warlock", 20, "Eldritch Master", "You can spend 1 minute entreating your patron for aid to regain all your expended spell slots."),

        # --- WIZARD ---
        ("Wizard", 1, "Spellcasting", "As a student of arcane magic, you have a spellbook containing spells that show the first glimmerings of your true power."),
        ("Wizard", 1, "Arcane Recovery", "You have learned to regain some of your magical energy by studying your spellbook."),
        ("Wizard", 2, "Arcane Tradition", "When you reach 2nd level, you choose an arcane tradition, shaping your practice of magic."),
        ("Wizard", 18, "Spell Mastery", "You have achieved such mastery over certain spells that you can cast them at will."),
        ("Wizard", 20, "Signature Spells", "You gain mastery over two powerful spells and can cast them with little effort.")
    ]

    for class_name, level, feat_name, feat_desc in features_data:
        try:
            c_class = CharacterClass.objects.get(name=class_name)
            ClassFeature.objects.get_or_create(
                character_class=c_class,
                subclass=None, # To są cechy podstawowej klasy
                name=feat_name,
                defaults={
                    "description": feat_desc,
                    "level_unlocked": level
                }
            )
        except CharacterClass.DoesNotExist:
            print(f"Warning: Class {class_name} not found. Skipping feature {feat_name}.")

    # --- 3. AUTO-GENERATE ASI (ABILITY SCORE IMPROVEMENT) ---
    # Every class gets ASI at 4, 8, 12, 16, 19. 
    # Fighter gets extra at 6, 14. 
    # Rogue gets extra at 10.
    
    asi_levels_base = [4, 8, 12, 16, 19]
    
    for c_class in CharacterClass.objects.all():
        levels = asi_levels_base.copy()
        
        if c_class.name == "Fighter":
            levels.extend([6, 14])
        elif c_class.name == "Rogue":
            levels.extend([10])
            
        for lvl in levels:
            ClassFeature.objects.get_or_create(
                character_class=c_class,
                subclass=None,
                name="Ability Score Improvement",
                defaults={
                    "description": "You can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can't increase an ability score above 20 using this feature. Alternatively, you can choose a Feat.",
                    "level_unlocked": lvl
                }
            )

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_feat_character_feats_classfeature'), 
    ]

    operations = [
        migrations.RunPython(populate_features),
    ]