from django.db import migrations


def populate_backgrounds(apps, schema_editor):
    Background = apps.get_model("base", "Background")
    Skill = apps.get_model("base", "Skill")
    Item = apps.get_model("base", "Item")
    BackgroundSkill = apps.get_model("base", "BackgroundSkillProficiency")
    BackgroundEquipment = apps.get_model("base", "BackgroundStartingEquipment")
    Tool = apps.get_model("base", "Tool")
    BackgroundTool = apps.get_model("base", "BackgroundToolProficiency")

    # ------------------------------------------------------------------
    # Background definitions (PHB)
    # ------------------------------------------------------------------
    backgrounds = {
        "Acolyte": {
            "description": (
                "You have spent your life in the service of a temple to a specific god "
                "or pantheon of gods. You act as an intermediary between the realm of "
                "the holy and the mortal world."
            ),
            "feature_name": "Shelter of the Faithful",
            "feature_description": (
                "You and your companions can expect free healing and care at temples "
                "and shrines of your faith, and those who share your religion will "
                "support you."
            ),
            "skills": ["Insight", "Religion"],
            "tools": [],
            "equipment": [
                ("Holy Symbol", 1),
                ("Prayer Book", 1),
                ("Incense", 5),
                ("Vestments", 1),
                ("Common Clothes", 1),
                ("Gold", 15),
            ],
        },

        "Charlatan": {
            "description": (
                "You have always had a way with people. You know what makes them tick "
                "and how to pull their strings."
            ),
            "feature_name": "False Identity",
            "feature_description": (
                "You have created a second identity that includes documentation, "
                "established acquaintances, and disguises."
            ),
            "skills": ["Deception", "Sleight of Hand"],
            "tools": ["Thieves' Tools"],
            "equipment": [
                ("Fine Clothes", 1),
                ("Disguise Kit", 1),
                ("Forgery Kit", 1),
                ("Gold", 15),
            ],
        },

        "City Watch": {
            "description": (
                "You have served the community by standing watch, enforcing the law, "
                "and confronting dangers that threaten the peace."
            ),
            "feature_name": "Watcher's Eye",
            "feature_description": (
                "You can easily find the local outpost of the watch or a similar organization, "
                "and pick out the dens of criminal activity in a community."
            ),
            "skills": ["Athletics", "Insight"],
            "tools": [],
            "equipment": [
                ("Uniform", 1),
                ("Horn", 1),
                ("Manacles", 1),
                ("Gold", 10),
            ],
        },
        "Criminal": {
            "description": (
                "You are an experienced criminal with a history of breaking the law. "
                "You have spent a lot of time among other criminals and still have contacts within the criminal underworld."
            ),
            "feature_name": "Criminal Contact",
            "feature_description": (
                "You have a reliable and trustworthy contact who acts as your liaison to a network of other criminals."
            ),
            "skills": ["Deception", "Stealth"],
            "tools": ["Thieves' Tools", "Gaming Set (Dice)"],
            "equipment": [
                ("Crowbar", 1),
                ("Dark Common Clothes", 1),
                ("Gold", 15),
            ],
        },
        "Entertainer": {
            "description": (
                "You thrive in front of an audience. You know how to entrance, "
                "entertain, and inspire."
            ),
            "feature_name": "By Popular Demand",
            "feature_description": (
                "You can always find a place to perform, usually in an inn or tavern, "
                "and receive free lodging and food."
            ),
            "skills": ["Acrobatics", "Performance"],
            "tools": ["Disguise Kit", "Musical Instrument (Any)"],
            "equipment": [
                ("Musical Instrument", 1),
                ("Costume", 1),
                ("Gold", 15),
            ],
        },

        "Folk Hero": {
            "description": (
                "You come from a humble social rank, but you are destined for so much more."
            ),
            "feature_name": "Rustic Hospitality",
            "feature_description": (
                "Common folk will shelter you and your companions from danger."
            ),
            "skills": ["Animal Handling", "Survival"],
            "tools": ["Artisan's Tools (Any)"],
            "equipment": [
                ("Artisan's Tools", 1),
                ("Shovel", 1),
                ("Iron Pot", 1),
                ("Common Clothes", 1),
                ("Gold", 10),
            ],
        },

        "Guild Artisan": {
            "description": (
                "You are a member of an artisan guild, skilled in a particular field "
                "and closely associated with other artisans."
            ),
            "feature_name": "Guild Membership",
            "feature_description": (
                "Your guild provides you with lodging and food, and will support you "
                "in legal matters."
            ),
            "skills": ["Insight", "Persuasion"],
            "tools": ["Artisan's Tools (Any)"],
            "equipment": [
                ("Artisan's Tools", 1),
                ("Letter of Introduction", 1),
                ("Traveler's Clothes", 1),
                ("Gold", 15),
            ],
        },

        "Guild Merchant": {
            "description": (
                "Instead of crafting items, you belong to a guild of traders, caravan masters, "
                "or shopkeepers. You know how to move goods and people."
            ),
            "feature_name": "Guild Membership",
            "feature_description": (
                "Your guild provides you with lodging and food, and will support you "
                "in legal matters."
            ),
            "skills": ["Insight", "Persuasion"],
            "tools": ["Navigator's Tools"],
            "equipment": [
                ("Mule and Cart", 1),
                ("Letter of Introduction", 1),
                ("Traveler's Clothes", 1),
                ("Gold", 15),
            ],
        },

        "Haunted One": {
            "description": (
                "You are haunted by something so terrible that you dare not speak of it. "
                "You try to keep it at bay, but it is always there."
            ),
            "feature_name": "Heart of Darkness",
            "feature_description": (
                "Commoners will do what they can to help you, feeling a strange urge "
                "to aid you in your suffering. They will even fight for you if you are alone."
            ),
            "skills": ["Arcana", "Investigation"], 
            "tools": [],
            "equipment": [
                ("Monster Hunter's Pack", 1),
                ("Gothic Trinket", 1),
                ("Common Clothes", 1),
                ("Gold", 1), # Usually 1 sp, rounded to 1gp or 0 for simplicity
            ],
        },

        "Hermit": {
            "description": (
                "You lived in seclusion for a formative part of your life."
            ),
            "feature_name": "Discovery",
            "feature_description": (
                "You discovered a unique and powerful secret about the world."
            ),
            "skills": ["Medicine", "Religion"],
            "tools": ["Herbalism Kit"],
            "equipment": [
                ("Scroll Case", 1),
                ("Winter Blanket", 1),
                ("Common Clothes", 1),
                ("Herbalism Kit", 1),
                ("Gold", 5),
            ],
        },

        "Noble": {
            "description": (
                "You understand wealth, power, and privilege."
            ),
            "feature_name": "Position of Privilege",
            "feature_description": (
                "People are inclined to think the best of you and treat you with respect."
            ),
            "skills": ["History", "Persuasion"],
            "tools": [],
            "equipment": [
                ("Fine Clothes", 1),
                ("Signet Ring", 1),
                ("Scroll of Pedigree", 1),
                ("Gold", 25),
            ],
        },

        "Outlander": {
            "description": (
                "You grew up in the wilds, far from civilization."
            ),
            "feature_name": "Wanderer",
            "feature_description": (
                "You have an excellent memory for maps and geography, and can always "
                "find food and fresh water for yourself and others."
            ),
            "skills": ["Athletics", "Survival"],
            "tools": ["Musical Instrument (Any)"],
            "equipment": [
                ("Staff", 1),
                ("Hunting Trap", 1),
                ("Trophy from Animal", 1),
                ("Traveler's Clothes", 1),
                ("Gold", 10),
            ],
        },

        "Sage": {
            "description": (
                "You spent years learning the lore of the multiverse. You scoured "
                "manuscripts, studied scrolls, and listened to the greatest experts."
            ),
            "feature_name": "Researcher",
            "feature_description": (
                "When you attempt to learn or recall a piece of lore, if you do not know "
                "that information, you often know where and from whom you can obtain it."
            ),
            "skills": ["Arcana", "History"],
            "tools": [],
            "equipment": [
                ("Bottle of Black Ink", 1),
                ("Quill", 1),
                ("Small Knife", 1),
                ("Letter from a Dead Colleague", 1),
                ("Common Clothes", 1),
                ("Gold", 10),
            ],
        },

        "Sailor": {
            "description": (
                "You sailed on a seagoing vessel for years."
            ),
            "feature_name": "Ship's Passage",
            "feature_description": (
                "You can secure free passage on a sailing ship for yourself and companions."
            ),
            "skills": ["Athletics", "Perception"],
            "tools": ["Navigator's Tools"],
            "equipment": [
                ("Belaying Pin", 1),
                ("Silk Rope (50 ft)", 1),
                ("Lucky Charm", 1),
                ("Common Clothes", 1),
                ("Gold", 10),
            ],
        },

        "Soldier": {
            "description": (
                "War has been your life for as long as you care to remember."
            ),
            "feature_name": "Military Rank",
            "feature_description": (
                "You have a military rank from your career as a soldier."
            ),
            "skills": ["Athletics", "Intimidation"],
            "tools": ["Gaming Set (Any)"],
            "equipment": [
                ("Insignia of Rank", 1),
                ("Trophy from Fallen Enemy", 1),
                ("Common Clothes", 1),
                ("Gold", 10),
            ],
        },

        "Urchin": {
            "description": (
                "You grew up on the streets alone, poor, and forgotten."
            ),
            "feature_name": "City Secrets",
            "feature_description": (
                "You know the secret patterns and flow of cities."
            ),
            "skills": ["Sleight of Hand", "Stealth"],
            "tools": ["Disguise Kit", "Thieves' Tools"],
            "equipment": [
                ("Small Knife", 1),
                ("Map of City", 1),
                ("Pet Mouse", 1),
                ("Common Clothes", 1),
                ("Gold", 10),
            ],
        },
    }

    # ------------------------------------------------------------------
    # Create data
    # ------------------------------------------------------------------
    for name, data in backgrounds.items():
        background, _ = Background.objects.get_or_create(
            name=name,
            defaults={
                "description": data["description"],
                "feature_name": data["feature_name"],
                "feature_description": data["feature_description"],
            },
        )

        # Skills
        for skill_name in data["skills"]:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            BackgroundSkill.objects.get_or_create(
                background=background,
                skill=skill,
            )

        # Equipment
        for item_name, qty in data["equipment"]:
            item, _ = Item.objects.get_or_create(
                name=item_name,
                defaults={"weight": 0, "value": 0},
            )
            BackgroundEquipment.objects.get_or_create(
                background=background,
                item=item,
                defaults={"quantity": qty},
            )

        for tool_name in data.get("tools", []):
            tool, _ = Tool.objects.get_or_create(name=tool_name)
            BackgroundTool.objects.get_or_create(
                background=background,
                tool=tool,
            )


def reverse_backgrounds(apps, schema_editor):
    Background = apps.get_model("base", "Background")
    Background.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0009_background_skill_tool_alter_character_background_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_backgrounds, reverse_backgrounds),
    ]
