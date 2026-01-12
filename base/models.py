from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q  # Needed for CheckConstraints

# --- Core Setup Models ---

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class CharacterClass(models.Model):
    """
    Replaces the old ClassChoices. 
    This allows us to link Spells directly to a Class in the database.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Character Classes"
        ordering = ['name']

class Spell(models.Model):
    """
    The Spell database. 
    Import your JSON data into this model using the script provided previously.
    """
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    school = models.CharField(max_length=50)
    cast_time = models.CharField(max_length=50)
    components = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    range_area = models.CharField(max_length=100)
    
    # Logic: A spell belongs to one or more classes (e.g., Light is for Bard, Cleric, etc.)
    available_to_classes = models.ManyToManyField(CharacterClass, related_name='spell_list')

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"

    class Meta:
        ordering = ['level', 'name']

# --- Choices ---

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

# --- Main Character Model ---

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    
    # CHANGED: Now a ForeignKey to the CharacterClass model
    # This enables: my_character.character_class.spell_list.all()
    character_class = models.ForeignKey(
        CharacterClass, 
        on_delete=models.PROTECT, 
        related_name='characters'
    )
    
    subclass = models.CharField(max_length=100) # class should be connected to subclass
    
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
    
    # Attributes
    strength = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    dexterity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    constitution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    intelligence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    wisdom = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    charisma = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    
    # Stats
    armor_class = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    initiative = models.IntegerField()
    speed = models.IntegerField(validators=[MinValueValidator(1)])
    hit_points = models.IntegerField(validators=[MinValueValidator(1)])
    temporary_hit_points = models.IntegerField(validators=[MinValueValidator(0)])
    hit_dice = models.IntegerField(validators=[MinValueValidator(1)])
    
    death_saves_success = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)])
    death_saves_failure = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)])
    
    backstory = models.TextField(null=True, blank=True) 
    inspiration = models.BooleanField(default=False)
    
    # Relationships
    languages = models.ManyToManyField(Language, blank=True)
    
    # NEW: This stores the specific spells this character has learned/prepared
    spells = models.ManyToManyField(Spell, blank=True, related_name='learned_by_characters')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.character_name} ({self.character_class}), Lvl {self.level}"
    
    class Meta:
        ordering = ['created_at']
        constraints = [
            models.CheckConstraint(condition=Q(level__gte=1) & Q(level__lte=20), name='level_range'),
            models.CheckConstraint(condition=Q(experience_points__gte=0), name='experience_points_minimum'),
            models.CheckConstraint(condition=Q(strength__gte=1) & Q(strength__lte=30), name='strength_range'),
            models.CheckConstraint(condition=Q(dexterity__gte=1) & Q(dexterity__lte=30), name='dexterity_range'),
            models.CheckConstraint(condition=Q(constitution__gte=1) & Q(constitution__lte=30), name='constitution_range'),
            models.CheckConstraint(condition=Q(intelligence__gte=1) & Q(intelligence__lte=30), name='intelligence_range'),
            models.CheckConstraint(condition=Q(wisdom__gte=1) & Q(wisdom__lte=30), name='wisdom_range'),
            models.CheckConstraint(condition=Q(charisma__gte=1) & Q(charisma__lte=30), name='charisma_range'),
            models.CheckConstraint(condition=Q(armor_class__gte=1) & Q(armor_class__lte=100), name='armor_class_range'),
            models.CheckConstraint(condition=Q(speed__gte=1), name='speed_minimum'),
            models.CheckConstraint(condition=Q(hit_points__gte=1), name='hit_points_minimum'),
            models.CheckConstraint(condition=Q(temporary_hit_points__gte=0), name='temporary_hit_points_minimum'),
            models.CheckConstraint(condition=Q(hit_dice__gte=1), name='hit_dice_minimum'),
            models.CheckConstraint(condition=Q(death_saves_success__gte=0) & Q(death_saves_success__lte=3), name='death_saves_success_range'),
            models.CheckConstraint(condition=Q(death_saves_failure__gte=0) & Q(death_saves_failure__lte=3), name='death_saves_failure_range'),
        ]