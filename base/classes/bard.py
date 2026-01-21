from django.db import models

class Bard(models.Model):
    SUBCLASS_CHOICES = [
        ('lore', 'College of Lore'),
        ('valor', 'College of Valor'),
        ('glamour', 'College of Glamour'),
    ]
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='bard_profile'
    )
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='lore'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"