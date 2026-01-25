from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator # type: ignore
from django.core.exceptions import ValidationError

class Background(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(help_text="General description of the background")
    feature_name = models.CharField(max_length=100, help_text="Name of the background feature")
    feature_description = models.TextField(help_text="Rules text of the background feature")

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

    # This handles "Which classes CAN learn this spell"
    dnd_classes = models.ManyToManyField(
        'CharacterClass',
        through='ClassSpell',
        related_name='spells'
    )

    def __str__(self):
        return self.name
# --- Spell Tables Constants ---
SPELLS_KNOWN_TABLE = {
    'Bard': {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 14, 11: 15, 12: 15, 13: 16, 14: 18, 15: 19, 16: 19, 17: 20, 18: 22, 19: 22, 20: 22},
    'Sorcerer': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 12, 13: 13, 14: 13, 15: 14, 16: 14, 17: 15, 18: 15, 19: 15, 20: 15},
    'Warlock': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10, 11: 11, 12: 11, 13: 12, 14: 12, 15: 13, 16: 13, 17: 14, 18: 14, 19: 15, 20: 15},
    'Ranger': {1: 0, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8, 14: 8, 15: 9, 16: 9, 17: 10, 18: 10, 19: 11, 20: 11},
    # Paladin/Cleric/Druid/Wizard are calculated dynamically
}

CANTRIPS_KNOWN_TABLE = {
    'Bard': {1: 2, 4: 3, 10: 4},
    'Cleric': {1: 3, 4: 4, 10: 5},
    'Druid': {1: 2, 4: 3, 10: 4},
    'Sorcerer': {1: 4, 4: 5, 10: 6},
    'Warlock': {1: 2, 4: 3, 10: 4},
    'Wizard': {1: 3, 4: 4, 10: 5},
}

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

    
    spells = models.ManyToManyField(Spell, blank=True, related_name='learned_by_characters')


    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.armor_class = self.total_armor_class
        self.initiative = self.calculate_initiative

        self.speed = 30 # Default speed, update logic if needed
        self.hit_dice = self.calculate_hit_dice
        # Only recalc max HP if it's 0 or None to avoid overwriting current HP during gameplay
        if not self.hit_points: 
            self.hit_points = self.calculate_hit_points
            
        # Ensure these default to 0 if not set
        if self.temporary_hit_points is None: self.temporary_hit_points = 0
        if self.death_saves_success is None: self.death_saves_success = 0
        if self.death_saves_failure is None: self.death_saves_failure = 0

        super().save(*args, **kwargs)
        
        # Assign starting equipment only when character is first created
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
        class_hit_dice = {
            'Barbarian': 12, 'Bard': 8, 'Cleric': 8, 'Druid': 8, 'Fighter': 10,
            'Monk': 8, 'Paladin': 10, 'Ranger': 10, 'Rogue': 8, 'Sorcerer': 6,
            'Warlock': 8, 'Wizard': 6,
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
        dex_mod = (self.dexterity - 10) // 2
        wis_mod = (self.wisdom - 10) // 2
        con_mod = (self.constitution - 10) // 2
        char_class = self.character_class.name.lower() if self.character_class else ""
        if char_class == "monk":
            return 10 + dex_mod + wis_mod
        elif char_class == "barbarian":
            return 10 + dex_mod + con_mod
        return 10 + dex_mod
        """
        Calculates total Armor Class (AC) based on character class and features.
        Default: 10 + DEX mod
        Monk: 10 + DEX mod + WIS mod (if not wearing armor)
        Barbarian: 10 + DEX mod + CON mod (if not wearing armor)
        Extend as needed for other classes/features.
        """       
    @property
    def proficiency_bonus(self):
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
        skills = Skill.objects.none()
        if self.background:
            skills |= Skill.objects.filter(backgroundskillproficiency__background=self.background)
        skills |= Skill.objects.filter(characterskillproficiency__character=self)
        return skills.distinct()
    
    def get_background_skill_proficiencies(self):
        # Fix: self.background is a ForeignKey, so we can access it directly if not null
        if not self.background:
            return Skill.objects.none()
        return Skill.objects.filter(backgroundskillproficiency__background=self.background)

# --- SPELL LOGIC START ---

    @property
    def max_cantrips_known(self):
        """Returns the maximum number of cantrips a character can know."""
        if not self.character_class:
            return 0
        
        char_class = self.character_class.name
        if char_class in CANTRIPS_KNOWN_TABLE:
            table = CANTRIPS_KNOWN_TABLE[char_class]
            # Find the highest level threshold met
            known = 0
            for lvl_threshold in sorted(table.keys()):
                if self.level >= lvl_threshold:
                    known = table[lvl_threshold]
            return known
        return 0

    @property
    def max_spells_known(self):
        """
        Returns the maximum number of leveled spells (1+) a character can know or prepare.
        Returns a tuple: (limit, limit_type) where limit_type is "Known" or "Prepared".
        """
        if not self.character_class:
            return 0, "None"

        char_class = self.character_class.name
        
        # A) Prepared Casters (Level + Ability Mod)
        if char_class in ['Cleric', 'Druid', 'Wizard']:
            modifier = 0
            if char_class == 'Wizard':
                modifier = self.get_ability_modifier('intelligence')
            else:
                modifier = self.get_ability_modifier('wisdom')
            
            # Minimum 1 spell
            return max(1, self.level + modifier), "Prepared"
        
        elif char_class == 'Paladin':
            modifier = self.get_ability_modifier('charisma')
            return max(1, (self.level // 2) + modifier), "Prepared"

        # B) Known Casters (Fixed Table)
        elif char_class in SPELLS_KNOWN_TABLE:
            return SPELLS_KNOWN_TABLE[char_class].get(self.level, 0), "Known"

        return 0, "None"

    # Note: Validating ManyToMany relationships in save() is impossible because 
    # the object must be saved before you can add M2M relations.
    # We create a custom validation method to be called in forms or views.
    def validate_spell_choices(self):
        """
        Checks if the currently assigned spells exceed class limits.
        Raises ValidationError if limits are exceeded.
        """
        if not self.pk:
            return # Cannot check relations on unsaved object

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

    # --- SPELL LOGIC END ---
    def __str__(self):
        return f"{self.character_name} ({self.character_class} Lvl {self.level})"
    
    class Meta:
        ordering = ['created_at']
        constraints = [
            models.CheckConstraint(condition=models.Q(level__gte=1) & models.Q(level__lte=20), name='level_range'),
            # ... (kept other constraints same as provided) ...
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

class ClassSpell(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
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
    background = models.ForeignKey(Background, on_delete=models.CASCADE, related_name='starting_equipment')
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