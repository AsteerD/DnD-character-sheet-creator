from django.db import models

class Rogue(models.Model):
    SUBCLASS_CHOICES = [
        ('thief', 'Thief'),
        ('assassin', 'Assassin'),
        ('trickster', 'Arcane Trickster'),
    ]

    # Używamy stringa, by uniknąć problemów z importem
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='rogue_profile'
    )
    
    # Tylko wybór subklasy - bonusy będą liczone w innym miejscu w przyszłości
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='thief'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"