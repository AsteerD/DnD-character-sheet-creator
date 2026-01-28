from django.contrib import admin # type: ignore
from .models import Character, Language, Subclass, CharacterClass, StartingEquipment, ClassSpell, Item, InventoryItem, Background, BackgroundStartingEquipment, Skill, Tool, BackgroundSkillProficiency, BackgroundToolProficiency, CharacterSkillProficiency, ClassSkillChoice, ClassFeature, Race 
 
admin.site.register(Character)
# Register your models here.

admin.site.register(Language)
admin.site.register(Subclass)
admin.site.register(CharacterClass)
admin.site.register(StartingEquipment)
admin.site.register(ClassSpell)
admin.site.register(Item)
admin.site.register(InventoryItem)
admin.site.register(Background)
admin.site.register(BackgroundStartingEquipment)
admin.site.register(Skill)
admin.site.register(Tool)
admin.site.register(BackgroundSkillProficiency)
admin.site.register(BackgroundToolProficiency)
admin.site.register(CharacterSkillProficiency)
admin.site.register(ClassSkillChoice)
admin.site.register(ClassFeature)
admin.site.register(Race)