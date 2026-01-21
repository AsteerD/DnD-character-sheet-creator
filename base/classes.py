# base/classes.py
from django.db import models

class Rogue(models.Model):
    SUBCLASS_CHOICES = [
        ('thief', 'Thief'),
        ('assassin', 'Assassin'),
        ('trickster', 'Arcane Trickster'),
    ]

    # Używamy stringa 'base.Character', aby uniknąć problemów z importem
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='rogue_profile'
    )
    
    # Podstawowy bonus wynikający z treningu (np. Twoje +5)
    stealth_bonus = models.IntegerField(default=5)
    
    # Bonus od szefa kampanii lub przedmiotów (np. buty elfa +3)
    magic_item_bonus = models.IntegerField(default=0)
    
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='thief'
    )

    def total_stealth_bonus(self):
        """Sumuje wszystkie możliwe bonusy do skradania"""
        return self.stealth_bonus + self.magic_item_bonus

    def backstab_damage(self):
        """Oblicza obrażenia ataku ukradkowego"""
        # Pobieramy sumę wszystkich bonusów
        bonus = self.total_stealth_bonus()
        dex = self.character.dexterity
        
        # Logika zależna od subklasy
        if self.subclass_type == 'assassin':
            # Zabójca zadaje potrójne obrażenia ze zręczności
            return (dex * 3) + bonus
        elif self.subclass_type == 'trickster':
            # Trickster dodaje inteligencję do standardowego ataku
            intel = self.character.intelligence
            return (dex * 2) + bonus + intel
        else:
            # Standardowy Thief (standardowy mnożnik x2)
            return (dex * 2) + bonus

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"
    
class Cleric(models.Model):
    DOMAIN_CHOICES = [
        ('life', 'Life Domain'),
        ('war', 'War Domain'),
        ('light', 'Light Domain'),
    ]

    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='cleric_profile'
    )
    
    # Klerycy polegają na Mądrości (Wisdom)
    holy_symbol_bonus = models.IntegerField(default=2) # Bonus od relikwii
    domain = models.CharField(
        max_length=20, 
        choices=DOMAIN_CHOICES, 
        default='life'
    )

    def healing_power(self):
        """Oblicza bazową moc leczenia"""
        wisdom_mod = (self.character.wisdom - 10) // 2 # Standardowy przelicznik D&D
        base_heal = wisdom_mod + self.holy_symbol_bonus
        
        if self.domain == 'life':
            # Domena Życia leczy mocniej (Bonus: 2 + poziom czaru, przyjmijmy stałe +3)
            return base_heal + 3
        return base_heal

    def armor_bonus(self):
        """Domena Wojny daje bonus do obrony"""
        if self.domain == 'war':
            return 2 # Bonus do AC za ciężką zbroję/tarczę
        return 0

    def __str__(self):
        return f"{self.character.character_name} - {self.get_domain_display()}"