from django.db import models

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
    
    domain = models.CharField(
        max_length=20, 
        choices=DOMAIN_CHOICES, 
        default='life'
    )

    def __str__(self):
        return f"{self.character.character_name} - {self.get_domain_display()}"