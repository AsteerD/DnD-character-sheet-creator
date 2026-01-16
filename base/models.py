from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore

# Create your models here.

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
    
class ClassChoices(models.TextChoices):
    BARBARIAN = 'Barbarian', 'Barbarian'
    BARD = 'Bard', 'Bard'
    CLERIC = 'Cleric', 'Cleric'
    DRUID = 'Druid', 'Druid'
    FIGHTER = 'Fighter', 'Fighter'
    MONK = 'Monk', 'Monk'
    PALADIN = 'Paladin', 'Paladin'
    RANGER = 'Ranger', 'Ranger'
    ROGUE = 'Rogue', 'Rogue'
    SORCERER = 'Sorcerer', 'Sorcerer'
    WARLOCK = 'Warlock', 'Warlock'
    WIZARD = 'Wizard', 'Wizard'


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

class SubclassChoices(models.TextChoices):
    # Rogue Subclasses
    THIEF = 'thief', 'Thief'
    ASSASSIN = 'assassin', 'Assassin'
    ARCANE_TRICKSTER = 'trickster', 'Arcane Trickster'
    
    # Fighter Subclasses (przykład na przyszłość)
    CHAMPION = 'champion', 'Champion'
    BATTLE_MASTER = 'battle_master', 'Battle Master'
    
    NONE = 'none', 'None'


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    character_class = models.CharField(
        max_length=20,
        choices=ClassChoices.choices,
        default=ClassChoices.FIGHTER,
    )
    character_class = models.CharField(
        max_length=20,
        choices=ClassChoices.choices,
        default=ClassChoices.FIGHTER,
    )

    # To pole zastępuje Twoje stare 'subclass'
    subclass = models.CharField(
        max_length=30,
        choices=SubclassChoices.choices,
        default=SubclassChoices.NONE,
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
    alligment = models.CharField(
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

class Rogue(models.Model):
    # Definiujemy dostępne subklasy
    SUBCLASS_CHOICES = [
        ('thief', 'Thief'),
        ('assassin', 'Assassin'),
        ('trickster', 'Arcane Trickster'),
    ]

    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='rogue_profile')
    stealth_bonus = models.IntegerField(default=0)
    
    # Nowe pole wyboru subklasy
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='thief'
    )

    def backstab_damage(self):
        base_dmg = self.character.dexterity * 2 + self.stealth_bonus
        
        if self.subclass_type == 'assassin':
            # Assassin zadaje potrójne obrażenia ze zręczności
            return self.character.dexterity * 3 + self.stealth_bonus
        
        elif self.subclass_type == 'trickster':
            # Arcane Trickster dodaje bonus od inteligencji (jeśli ją masz w modelu Character)
            return base_dmg + self.character.intelligence
            
        # Thief zostaje przy standardowym wzorze
        return base_dmg

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"
    

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Character)
def create_character_profile(sender, instance, created, **kwargs):
    if created:
        # Wyświetl w konsoli co dokładnie jest w polu klasy (pomoże w debugowaniu)
        print(f"Tworzę postać: {instance.character_name}, Klasa: {instance.character_class}")
        
        # Twoja klasa ClassChoices pewnie przechowuje 'ROGUE' lub 'Rogue'
        # Sprawdzamy na oba sposoby:
        if str(instance.character_class).upper() == 'ROGUE':
            Rogue.objects.create(
                character=instance, 
                stealth_bonus=5, 
                subclass_type=instance.subclass 
            )
            print("Profil Rogue został stworzony automatycznie!")