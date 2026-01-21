from django.db import models

class Ranger(models.Model):
    SUBCLASS_CHOICES = [
        ('hunter', 'Hunter'),
        ('beast_master', 'Beast Master'),
        ('gloom_stalker', 'Gloom Stalker'),
    ]
    character = models.OneToOneField(
        'base.Character', 
        on_delete=models.CASCADE, 
        related_name='ranger_profile'
    )
    subclass_type = models.CharField(
        max_length=20, 
        choices=SUBCLASS_CHOICES, 
        default='hunter'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_subclass_type_display()}"