from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore

class Background(models.Model):
    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(
        help_text="General description of the background"
    )

    feature_name = models.CharField(
        max_length=100,
        help_text="Name of the background feature (e.g. Shelter of the Faithful)"
    )

    feature_description = models.TextField(
        help_text="Rules text of the background feature"
    )

    def __str__(self):
        return self.name


class AbilityScoreChoices(models.TextChoices):
    STRENGTH = 'strength', 'Strength'
    DEXTERITY = 'dexterity', 'Dexterity'
    CONSTITUTION = 'constitution', 'Constitution'
    INTELLIGENCE = 'intelligence', 'Intelligence'
    WISDOM = 'wisdom', 'Wisdom'
    CHARISMA = 'charisma', 'Charisma'

class RaceChoices(models.TextChoices):
    AASIMAR = 'Aasimar', 'Aasimar'
    HUMAN = 'Human', 'Human'
    ELF = 'Elf', 'Elf'
    DWARF = 'Dwarf', 'Dwarf'
    HALFLING = 'Halfling', 'Halfling'
    GNOME = 'Gnome', 'Gnome'
    DRAGONBORN = 'Dragonborn', 'Dragonborn'
    TIEFLING = 'Tiefling', 'Tiefling'
    HALF_ELF = 'Half-Elf', 'Half-Elf'
    HALF_ORC = 'Half-Orc', 'Half-Orc'
    ORC = 'Orc', 'Orc'

class RaceModifier(models.Model):
    race = models.CharField(max_length=30, choices=RaceChoices.choices)
    ability = models.CharField(max_length=20, choices=AbilityScoreChoices.choices)
    modifier = models.IntegerField()

    def __str__(self):
        return f"{self.race}: {self.ability} {self.modifier:+d}"

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Alignment(models.TextChoices):
    LAWFUL_GOOD = 'LG', 'Lawful Good'
    NEUTRAL_GOOD = 'NG', 'Neutral Good'
    CHAOTIC_GOOD = 'CG', 'Chaotic Good'
    LAWFUL_NEUTRAL = 'LN', 'Lawful Neutral'
    TRUE_NEUTRAL = 'TN', 'True Neutral'
    CHAOTIC_NEUTRAL = 'CN', 'Chaotic Neutral'
    LAWFUL_EVIL = 'LE', 'Lawful Evil'
    NEUTRAL_EVIL = 'NE', 'Neutral Evil'
    CHAOTIC_EVIL = 'CE', 'Chaotic Evil'


class StartingEquipment(models.Model):
    character_class = models.ForeignKey('CharacterClass', on_delete=models.CASCADE, related_name='starting_equipment')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.character_class}: {self.item} x{self.quantity}"

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ability = models.CharField(
        max_length=20,
        choices=AbilityScoreChoices.choices,
        default=AbilityScoreChoices.DEXTERITY,
    )

    def __str__(self):
        return self.name

class Character(models.Model):
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.armor_class = self.total_armor_class
        self.initiative = self.calculate_initiative

        self.speed = 30
        self.hit_dice = self.calculate_hit_dice
        self.hit_points = self.calculate_hit_points
        self.temporary_hit_points = 0
        self.death_saves_success = 0
        self.death_saves_failure = 0

        super().save(*args, **kwargs)
        # Assign starting equipment only when character is first created
        if is_new:
            equipment_qs = StartingEquipment.objects.filter(character_class=self.character_class)
            for eq in equipment_qs:
                InventoryItem.objects.create(character=self, item=eq.item, quantity=eq.quantity)

            # background equipment
            bg_equipment = BackgroundStartingEquipment.objects.filter(background=self.background)
            for eq in bg_equipment:
                InventoryItem.objects.create(
                    character=self,
                    item=eq.item,
                    quantity=eq.quantity
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)

    character_class = models.ForeignKey(
        'CharacterClass',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
    )

    subclass = models.ForeignKey(
        'Subclass',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
        help_text='Subclass of the character (optional)'
    )

    race = models.CharField(
        max_length=30,
        choices=RaceChoices.choices,
        default=RaceChoices.HUMAN,
    )

    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    background = models.ForeignKey(
        Background,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
    )
    alignment = models.CharField(
        max_length=2,
        choices=Alignment.choices,
        default=Alignment.TRUE_NEUTRAL,
    )
    experience_points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    strength = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    dexterity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    constitution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    intelligence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    wisdom = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    charisma = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    armor_class = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=True, editable=False, default=10)
    initiative = models.IntegerField()
    speed = models.IntegerField(validators=[MinValueValidator(1)])
    hit_points = models.IntegerField(validators=[MinValueValidator(1)])
    temporary_hit_points = models.IntegerField(validators=[MinValueValidator(0)])
    hit_dice = models.IntegerField(validators=[MinValueValidator(1)])
    death_saves_success = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)])
    death_saves_failure = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)] )
    backstory = models.TextField(null=True, blank=True)
    inspiration = models.BooleanField(default=False)
    languages = models.ManyToManyField(Language, blank=True)

    @property
    def calculate_initiative(self):
        """
        Calculates total Initiative based on character class and features.
        Default: DEX mod
        Extend as needed for other classes/features.
        """
        dex_mod = (self.dexterity - 10) // 2
        return dex_mod

    @property
    def calculate_hit_dice(self):
        class_hit_dice = {
            'Barbarian': 12,
            'Bard': 8,
            'Cleric': 8,
            'Druid': 8,
            'Fighter': 10,
            'Monk': 8,
            'Paladin': 10,
            'Ranger': 10,
            'Rogue': 8,
            'Sorcerer': 6,
            'Warlock': 8,
            'Wizard': 6,
        }
        if self.character_class and self.character_class.name in class_hit_dice:
            return class_hit_dice[self.character_class.name]
        return 8

    @property
    def calculate_hit_points(self):
        con_mod = (self.constitution - 10) // 2
        hit_die = self.calculate_hit_dice
        return hit_die + con_mod + ( (self.level - 1) * ( (hit_die // 2) + 1 + con_mod ) )

    @property
    def total_armor_class(self):
        """
        Calculates total Armor Class (AC) based on character class and features.
        Default: 10 + DEX mod
        Monk: 10 + DEX mod + WIS mod (if not wearing armor)
        Barbarian: 10 + DEX mod + CON mod (if not wearing armor)
        Extend as needed for other classes/features.
        """
        dex_mod = (self.dexterity - 10) // 2
        wis_mod = (self.wisdom - 10) // 2
        con_mod = (self.constitution - 10) // 2
        char_class = self.character_class.name.lower() if self.character_class else ""
        if char_class == "monk":
            return 10 + dex_mod + wis_mod
        elif char_class == "barbarian":
            return 10 + dex_mod + con_mod
        return 10 + dex_mod

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def proficiency_bonus(self):
        # D&D 5e
        return 2 + (self.level - 1) // 4

    def get_ability_modifier(self, ability_name: str) -> int:
        score = getattr(self, ability_name)
        return (score - 10) // 2

    def get_skill_bonus(self, skill: Skill) -> int:
        bonus = self.get_ability_modifier(skill.ability)

        if skill in self.get_skill_proficiencies():
            bonus += self.proficiency_bonus

        return bonus

    def get_skill_proficiencies(self):
        """
        Skille, w których postać ma proficiency
        (background + wybory gracza)
        """
        skills = Skill.objects.none()

        # background (automatycznie)
        if self.background:
            skills |= Skill.objects.filter(
                backgroundskillproficiency__background=self.background
            )

        # wybory gracza (klasa)
        skills |= Skill.objects.filter(
            characterskillproficiency__character=self
        )

        return skills.distinct()

    def get_background_skill_proficiencies(self):
        background = Background.objects.filter(name=self.background).first()
        if not background:
            return Skill.objects.none()

        return Skill.objects.filter(
            backgroundskillproficiency__background=background
        )

    # def get_character_class_display(self):
    #     return "<button class='button'></button>"

    def __str__(self):
        return f"{self.character_name}, {self.created_at}, {self.user}, {self.character_class}"

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.CheckConstraint(condition=models.Q(level__gte=1) & models.Q(level__lte=20), name='level_range'),
            models.CheckConstraint(condition=models.Q(experience_points__gte=0), name='experience_points_minimum'),
            models.CheckConstraint(condition=models.Q(strength__gte=1) & models.Q(strength__lte=30), name='strength_range'),
            models.CheckConstraint(condition=models.Q(dexterity__gte=1) & models.Q(dexterity__lte=30), name='dexterity_range'),
            models.CheckConstraint(condition=models.Q(constitution__gte=1) & models.Q(constitution__lte=30), name='constitution_range'),
            models.CheckConstraint(condition=models.Q(intelligence__gte=1) & models.Q(intelligence__lte=30), name='intelligence_range'),
            models.CheckConstraint(condition=models.Q(wisdom__gte=1) & models.Q(wisdom__lte=30), name='wisdom_range'),
            models.CheckConstraint(condition=models.Q(charisma__gte=1) & models.Q(charisma__lte=30), name='charisma_range'),
            models.CheckConstraint(condition=models.Q(armor_class__gte=1) & models.Q(armor_class__lte=100), name='armor_class_range'),
            models.CheckConstraint(condition=models.Q(speed__gte=1), name='speed_minimum'),
            models.CheckConstraint(condition=models.Q(hit_points__gte=1), name='hit_points_minimum'),
            models.CheckConstraint(condition=models.Q(temporary_hit_points__gte=0), name='temporary_hit_points_minimum'),
            models.CheckConstraint(condition=models.Q(hit_dice__gte=1), name='hit_dice_minimum'),
            models.CheckConstraint(condition=models.Q(death_saves_success__gte=0) & models.Q(death_saves_success__lte=3), name='death_saves_success_range'),
            models.CheckConstraint(condition=models.Q(death_saves_failure__gte=0) & models.Q(death_saves_failure__lte=3), name='death_saves_failure_range'),
        ]

class CharacterClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    skill_choices_count = models.IntegerField(default=2)

    def __str__(self):
        return self.name

class Subclass(models.Model):
    name = models.CharField(max_length=50)
    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.CASCADE,
        related_name='subclasses'
    )

    def __str__(self):
        return f"{self.character_class}: {self.name}"

class Spell(models.Model):
    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField()
    higher_level = models.TextField(blank=True, null=True)
    page = models.CharField(max_length=50)
    range = models.CharField(max_length=100)
    components = models.CharField(max_length=255)
    material = models.CharField(max_length=255, blank=True, null=True)
    ritual = models.BooleanField(default=False)
    duration = models.CharField(max_length=100)
    concentration = models.BooleanField(default=False)
    casting_time = models.CharField(max_length=100)
    level = models.IntegerField()
    school = models.CharField(max_length=100)

    dnd_classes = models.ManyToManyField(
        CharacterClass,
        through='ClassSpell',
        related_name='spells'
    )

    def __str__(self):
        return self.name

class ClassSpell(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)

    # 👇 NOWE
    subclass = models.ForeignKey(
        Subclass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Jeśli null → spell dostępny dla całej klasy"
    )

    unlock_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['spell', 'character_class', 'subclass'],
                name='unique_spell_class_subclass'
            )
        ]
        ordering = ['unlock_level']

    def __str__(self):
        if self.subclass:
            return f"{self.character_class}/{self.subclass} → {self.spell} (lvl {self.unlock_level})"
        return f"{self.character_class} → {self.spell} (lvl {self.unlock_level})"

class Item(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"


class BackgroundStartingEquipment(models.Model):
    background = models.ForeignKey(
        Background,
        on_delete=models.CASCADE,
        related_name='starting_equipment'
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.background}: {self.item} x{self.quantity}"

class Tool(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BackgroundSkillProficiency(models.Model):
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class BackgroundToolProficiency(models.Model):
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

class CharacterSkillProficiency(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('character', 'skill')

class ClassSkillChoice(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
