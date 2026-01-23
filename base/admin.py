from django.contrib import admin # type: ignore
from .models import Character, Language, Subclass, CharacterClass, StartingEquipment, ClassSpell, Item, InventoryItem

admin.site.register(Character)
# Register your models here.

admin.site.register(Language)
admin.site.register(Subclass)
admin.site.register(CharacterClass)
admin.site.register(StartingEquipment)
admin.site.register(ClassSpell)
admin.site.register(Item)
admin.site.register(InventoryItem)

