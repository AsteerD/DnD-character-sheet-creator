from django.db import models

class Fighter(models.Model):
    SUBCLASS_CHOICES = [
        ('champion', 'Champion'),
        ('battle_master', 'Battle Master'),
        ('eldritch_knight', 'Eldritch Knight'),
    ]
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='fighter_profile'
    )
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='champion'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"