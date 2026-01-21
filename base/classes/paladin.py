from django.db import models

class Paladin(models.Model):
    SUBCLASS_CHOICES = [
        ('devotion', 'Oath of Devotion'),
        ('ancients', 'Oath of the Ancients'),
        ('vengeance', 'Oath of Vengeance'),
    ]
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='paladin_profile'
    )
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='devotion'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"