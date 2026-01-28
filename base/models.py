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

class Race(models.Model):
    name = models.CharField(max_length=50, unique=True)
    speed = models.PositiveIntegerField(default=30, help_text="Base walking speed in feet")

    def __str__(self):
        return self.name

class RaceModifier(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='modifiers')
    ability = models.CharField(max_length=20, choices=AbilityScoreChoices.choices)
    modifier = models.IntegerField()

    def __str__(self):
        return f"{self.race.name}: {self.ability} {self.modifier:+d}"

class CharacterClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Class configuration fields
    hit_die = models.IntegerField(help_text="Hit die value, e.g., 8 for d8, 12 for d12", default=8)
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
    # Additional field for AC (Monk/Barbarian)
    unarmored_bonus_ability = models.CharField(
        max_length=20, 
        choices=AbilityScoreChoices.choices, 
        null=True, blank=True,
        help_text="Ability that adds to AC when unarmored (e.g. Wisdom for Monk)"
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

class Feat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    prerequisite = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. 'Dexterity 13' or 'Elf'")
    
    def __str__(self):
        return self.name

class ClassFeature(models.Model):
    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.CASCADE,
        related_name="class_features"
    )
    subclass = models.ForeignKey(
        Subclass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Null = base class feature"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    unlock_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    class Meta:
        ordering = ["unlock_level"]
        constraints = [
            models.UniqueConstraint(
                fields=["character_class", "subclass", "name"],
                name="unique_class_feature"
            )
        ]

    def __str__(self):
        if self.subclass:
            return f"{self.character_class}/{self.subclass} – {self.name} (lvl {self.unlock_level})"
        return f"{self.character_class} – {self.name} (lvl {self.unlock_level})"

class ClassSpellProgression(models.Model):
    """
    Data-driven table for spell slots and known spells/cantrips per level.
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
        'CharacterClass',
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

    race = models.ForeignKey(Race, on_delete=models.PROTECT, null=True, blank=True)
    
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
    
    feats = models.ManyToManyField(Feat, blank=True, related_name='characters')

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

    @property
    def total_strength(self):
        return self.strength + self.get_racial_bonus('strength')

    @property
    def total_dexterity(self):
        return self.dexterity + self.get_racial_bonus('dexterity')
    
    @property
    def total_constitution(self):
        return self.constitution + self.get_racial_bonus('constitution')

    @property
    def total_intelligence(self):
        return self.intelligence + self.get_racial_bonus('intelligence')

    @property
    def total_wisdom(self):
        return self.wisdom + self.get_racial_bonus('wisdom')

    @property
    def total_charisma(self):
        return self.charisma + self.get_racial_bonus('charisma')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.armor_class = self.total_armor_class
        self.initiative = self.calculate_initiative

        # Speed from database
        if self.race:
            self.speed = self.race.speed

        if not is_new:
            try:
                old_instance = Character.objects.get(pk=self.pk)
                if old_instance.character_class != self.character_class:
                    self.spells.clear()
            except Character.DoesNotExist:
                pass

        # Hit Dice from database
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

    def get_racial_bonus(self, ability_name: str) -> int:
        """Returns the racial modifier for a given ability score."""
        if not self.race:
            return 0
        modifier_obj = self.race.modifiers.filter(ability=ability_name.lower()).first()
        return modifier_obj.modifier if modifier_obj else 0

    @property
    def calculate_initiative(self):
        dex_mod = (self.dexterity - 10) // 2
        return dex_mod
    
    @property
    def calculate_hit_dice(self):
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
        
        ac = 10 + dex_mod
        if self.character_class and self.character_class.unarmored_bonus_ability:
             bonus_stat = self.character_class.unarmored_bonus_ability
             ac += self.get_ability_modifier(bonus_stat)
        elif char_class_name == "monk": # Fallback
             ac += wis_mod
        elif char_class_name == "barbarian": # Fallback
             ac += con_mod
        return ac

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
    
    def get_class_features(self):
        if not self.character_class:
            return ClassFeature.objects.none()

        return ClassFeature.objects.filter(
            character_class=self.character_class,
            unlock_level__lte=self.level
        ).filter(
            Q(subclass__isnull=True) |
            Q(subclass=self.subclass)
        ).order_by('unlock_level')

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
        """
        if not self.character_class:
            return 0, "None"

        # 1. Prepared Casters
        if self.character_class.is_prepared_caster:
            ability_name = self.character_class.spellcasting_ability
            if not ability_name:
                return 0, "None"
            
            modifier = self.get_ability_modifier(ability_name)
            level_base = int(self.level * self.character_class.preparation_multiplier)
            return max(1, level_base + modifier), "Prepared"

        # 2. Known Casters
        try:
            progression = self.character_class.spell_progression.get(level=self.level)
            return progression.spells_known, "Known"
        except ClassSpellProgression.DoesNotExist:
            return 0, "None"

    def validate_spell_choices(self):
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