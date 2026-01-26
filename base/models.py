from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

# --- CONSTANTS & CHOICES ---

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

# --- CONFIGURATION MODELS ---

class CharacterClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hit_die = models.IntegerField(help_text="Hit die value, e.g., 8 for d8, 12 for d12")
    skill_choices_count = models.IntegerField(default=2)
    
    # Spellcasting Configuration
    spellcasting_ability = models.CharField(
        max_length=20, 
        choices=AbilityScoreChoices.choices,
        null=True, 
        blank=True, 
        help_text="Primary ability for spellcasting. Leave empty for non-casters."
    )
    is_prepared_caster = models.BooleanField(
        default=False,
        help_text="If True, spells prepared limit = (Level * Multiplier) + Mod. If False, limit is taken from the progression table."
    )
    preparation_multiplier = models.FloatField(
        default=1.0,
        help_text="Multiplier for prepared spells formula. Wizard/Cleric = 1.0, Paladin = 0.5."
    )

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
        return f"{self.character_class.name}: {self.name}"

class ClassSpellProgression(models.Model):
    """
    Data-driven table for spell slots and known spells/cantrips per level.
    Replaces hardcoded dictionaries.
    """
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name='spell_progression')
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    
    cantrips_known = models.IntegerField(default=0)
    spells_known = models.IntegerField(default=0, help_text="Fixed known spells (Bard/Sorcerer). Set 0 for Prepared casters.")
    
    # Spell Slots
    slots_level_1 = models.IntegerField(default=0)
    slots_level_2 = models.IntegerField(default=0)
    slots_level_3 = models.IntegerField(default=0)
    slots_level_4 = models.IntegerField(default=0)
    slots_level_5 = models.IntegerField(default=0)
    slots_level_6 = models.IntegerField(default=0)
    slots_level_7 = models.IntegerField(default=0)
    slots_level_8 = models.IntegerField(default=0)
    slots_level_9 = models.IntegerField(default=0)

    class Meta:
        unique_together = ('character_class', 'level')
        ordering = ['character_class', 'level']

    def __str__(self):
        return f"{self.character_class.name} Lvl {self.level}"

# --- GENERAL MODELS ---

class Background(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(help_text="General description of the background")
    feature_name = models.CharField(max_length=100, help_text="Name of the background feature")
    feature_description = models.TextField(help_text="Rules text of the background feature")

    def __str__(self):
        return self.name

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

class Item(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class StartingEquipment(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name='starting_equipment')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
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
    subclass = models.ForeignKey(
        Subclass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If null -> spell is available for the entire class"
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
            return f"{self.character_class}/{self.subclass} -> {self.spell} (lvl {self.unlock_level})"
        return f"{self.character_class} -> {self.spell} (lvl {self.unlock_level})"

class Race(models.Model):
    name = models.CharField(max_length=50, unique=True)
    speed = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"
    
class BackgroundStartingEquipment(models.Model):
    background = models.ForeignKey(Background, on_delete=models.CASCADE, related_name='starting_equipment')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.background}: {self.item} x{self.quantity}"

# --- PROFICIENCY MODELS ---

class BackgroundSkillProficiency(models.Model):
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class BackgroundToolProficiency(models.Model):
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

class CharacterSkillProficiency(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('character', 'skill')

class ClassSkillChoice(models.Model):
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

# --- CHARACTER MODEL ---

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)

    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
    )

    subclass = models.ForeignKey(
        Subclass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters',
        help_text='Subclass of the character (optional)'
    )

    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    
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
    
    # Abilities
    strength = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    dexterity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    constitution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    intelligence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    wisdom = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    charisma = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    
    # Computed Stats
    armor_class = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=True, editable=False, default=10)
    initiative = models.IntegerField()
    speed = models.IntegerField(validators=[MinValueValidator(1)], editable=False, default=30)
    hit_points = models.IntegerField(validators=[MinValueValidator(1)])
    temporary_hit_points = models.IntegerField(validators=[MinValueValidator(0)])
    hit_dice = models.IntegerField(validators=[MinValueValidator(1)])
    
    death_saves_success = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)])
    death_saves_failure = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(3)] )
    backstory = models.TextField(null=True, blank=True) 
    inspiration = models.BooleanField(default=False)
    languages = models.ManyToManyField(Language, blank=True)

    spells = models.ManyToManyField(Spell, blank=True, related_name='learned_by_characters')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.armor_class = self.total_armor_class
        self.initiative = self.calculate_initiative

        if self.race:
            self.speed = self.race.speed

        if not is_new:
            try:
                old_instance = Character.objects.get(pk=self.pk)
                if old_instance.character_class != self.character_class:
                    self.spells.clear()
            except Character.DoesNotExist:
                pass

        self.hit_dice = self.calculate_hit_dice
        
        if not self.hit_points: 
            self.hit_points = self.calculate_hit_points
            
        if self.temporary_hit_points is None: self.temporary_hit_points = 0
        if self.death_saves_success is None: self.death_saves_success = 0
        if self.death_saves_failure is None: self.death_saves_failure = 0

        super().save(*args, **kwargs)
        
        # Starting Equipment Logic
        if is_new:
            if self.character_class:
                equipment_qs = StartingEquipment.objects.filter(character_class=self.character_class)
                for eq in equipment_qs:
                    InventoryItem.objects.create(character=self, item=eq.item, quantity=eq.quantity)
    
            if self.background:
                bg_equipment = BackgroundStartingEquipment.objects.filter(background=self.background)
                for eq in bg_equipment:
                    InventoryItem.objects.create(
                        character=self,
                        item=eq.item,
                        quantity=eq.quantity
                    )

    @property
    def calculate_initiative(self):
        dex_mod = (self.dexterity - 10) // 2
        return dex_mod
    
    @property
    def calculate_hit_dice(self):
        # Database driven: no more dictionaries
        if self.character_class:
            return self.character_class.hit_die
        return 8
    
    @property
    def calculate_hit_points(self):
        con_mod = (self.constitution - 10) // 2
        hit_die = self.calculate_hit_dice
        return hit_die + con_mod + ( (self.level - 1) * ( (hit_die // 2) + 1 + con_mod ) )

    @property
    def total_armor_class(self):
        dex_mod = (self.dexterity - 10) // 2
        wis_mod = (self.wisdom - 10) // 2
        con_mod = (self.constitution - 10) // 2
        char_class_name = self.character_class.name.lower() if self.character_class else ""
        
        # Note: Ideally this logic should also be moved to CharacterClass fields (e.g., has_unarmored_defense=True)
        # to strictly follow "no hardcoded rules", but keeping it simple for now as per instructions.
        if char_class_name == "monk":
            return 10 + dex_mod + wis_mod
        elif char_class_name == "barbarian":
            return 10 + dex_mod + con_mod
        return 10 + dex_mod

    @property
    def proficiency_bonus(self):
        return 2 + (self.level - 1) // 4
    
    def get_ability_modifier(self, ability_name: str) -> int:
        score = getattr(self, ability_name.lower())
        return (score - 10) // 2

    def get_skill_bonus(self, skill: Skill) -> int:
        bonus = self.get_ability_modifier(skill.ability)
        if skill in self.get_skill_proficiencies():
            bonus += self.proficiency_bonus
        return bonus

    def get_skill_proficiencies(self):
        skills = Skill.objects.none()
        if self.background:
            skills |= Skill.objects.filter(backgroundskillproficiency__background=self.background)
        skills |= Skill.objects.filter(characterskillproficiency__character=self)
        return skills.distinct()
    
    def get_background_skill_proficiencies(self):
        if not self.background:
            return Skill.objects.none()
        return Skill.objects.filter(backgroundskillproficiency__background=self.background)

    # --- SPELL LOGIC (DATA DRIVEN) ---

    @property
    def max_cantrips_known(self):
        """Returns the maximum number of cantrips a character can know from database."""
        if not self.character_class:
            return 0
        
        try:
            progression = self.character_class.spell_progression.get(level=self.level)
            return progression.cantrips_known
        except ClassSpellProgression.DoesNotExist:
            return 0

    @property
    def max_spells_known(self):
        """
        Returns a tuple: (limit, limit_type)
        limit_type is "Known" (fixed list) or "Prepared" (daily selection).
        """
        if not self.character_class:
            return 0, "None"

        # 1. Prepared Casters (Cleric, Druid, Paladin, Wizard)
        if self.character_class.is_prepared_caster:
            ability_name = self.character_class.spellcasting_ability
            if not ability_name:
                return 0, "None"
            
            modifier = self.get_ability_modifier(ability_name)
            
            # Formula: (Level * Multiplier) + Mod
            # Wizard/Cleric: Multiplier 1.0 -> Level + Mod
            # Paladin: Multiplier 0.5 -> Level/2 + Mod
            level_base = int(self.level * self.character_class.preparation_multiplier)
            
            return max(1, level_base + modifier), "Prepared"

        # 2. Known Casters (Bard, Sorcerer, Warlock, Ranger) -> Read from DB Table
        try:
            progression = self.character_class.spell_progression.get(level=self.level)
            return progression.spells_known, "Known"
        except ClassSpellProgression.DoesNotExist:
            return 0, "None"

    def validate_spell_choices(self):
        """
        Validation method to be called in views/forms.
        """
        if not self.pk:
            return

        current_spells = self.spells.all()
        cantrips_count = current_spells.filter(level=0).count()
        leveled_count = current_spells.filter(level__gt=0).count()

        max_cantrips = self.max_cantrips_known
        max_spells, limit_type = self.max_spells_known

        errors = {}

        if max_cantrips > 0 and cantrips_count > max_cantrips:
            errors['cantrips'] = f"Too many Cantrips! Max {max_cantrips}, but you have {cantrips_count}."

        if max_spells > 0 and leveled_count > max_spells:
            errors['spells'] = f"Too many Spells! Max {max_spells} ({limit_type}), but you have {leveled_count}."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.character_name} ({self.character_class} Lvl {self.level})"
    
    class Meta:
        ordering = ['created_at']
        constraints = [
            models.CheckConstraint(condition=models.Q(level__gte=1) & models.Q(level__lte=20), name='level_range'),
        ]