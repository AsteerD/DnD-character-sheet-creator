from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "character_name",
            "character_class",
            "race",
            "background",
            "alignment",
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
            "backstory"
        ]
