from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore


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
    


class BackgroundChoices(models.TextChoices):
    ACOLYTE = 'Acolyte', 'Acolyte'
    CHARLATAN = 'Charlatan', 'Charlatan'
    CRIMINAL = 'Criminal', 'Criminal'
    ENTERTAINER = 'Entertainer', 'Entertainer'
    FOLK_HERO = 'Folk Hero', 'Folk Hero'
    GUILD_ARTISAN = 'Guild Artisan', 'Guild Artisan'
    HERMIT = 'Hermit', 'Hermit'
    NOBLE = 'Noble', 'Noble'
    OUTLANDER = 'Outlander', 'Outlander'
    SAGE = 'Sage', 'Sage'
    SAILOR = 'Sailor', 'Sailor'
    SOLDIER = 'Soldier', 'Soldier'
    URCHIN = 'Urchin', 'Urchin'
    HAUNTED_ONE = 'Haunted One', 'Haunted One'
    URBAN_BOUNTY_HUNTER = 'Urban Bounty Hunter', 'Urban Bounty Hunter'
    KNIGHT = 'Knight', 'Knight'
    FACTION_AGENT = 'Faction Agent', 'Faction Agent'
    MERCENARY_VETERAN = 'Mercenary Veteran', 'Mercenary Veteran'


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



class Character(models.Model):
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
    )
    

    race = models.CharField(
        max_length=30,
        choices=RaceChoices.choices,
        default=RaceChoices.HUMAN,
    )
    
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    background = models.CharField(
        max_length=30,
        choices=BackgroundChoices.choices,
        default=BackgroundChoices.ACOLYTE,
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
    armor_class = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
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
    def total_armor_class(self):
        dex_mod = (self.dexterity - 10) // 2
        return 10 + dex_mod

    created_at = models.DateTimeField(auto_now_add=True)

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