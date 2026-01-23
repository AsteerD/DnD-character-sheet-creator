from django.contrib import admin
from .models import (
    Character, CharacterClass, Subclass, Feat, Background,
    Item, InventoryItem, Spell, ClassSpell, Skill, Tool, Language,
    RaceModifier, StartingEquipment, BackgroundStartingEquipment,
    BackgroundSkillProficiency, BackgroundToolProficiency,
    CharacterSkillProficiency, ClassSkillChoice
)

# ==========================================
# 1. KONFIGURACJA INLINES (Edycja w środku rodzica)
# ==========================================

# Pozwala dodawać przedmioty bezpośrednio w widoku Postaci
class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1

# Pozwala dodawać skille bezpośrednio w widoku Postaci
class CharacterSkillProficiencyInline(admin.TabularInline):
    model = CharacterSkillProficiency
    extra = 1

# Pozwala dodawać podklasy bezpośrednio w widoku Klasy (np. Cleric -> Life Domain)
class SubclassInline(admin.TabularInline):
    model = Subclass
    extra = 1

# Pozwala przypisywać czary do klasy
class ClassSpellInline(admin.TabularInline):
    model = ClassSpell
    extra = 1

# Pozwala definiować ekwipunek startowy dla klasy
class StartingEquipmentInline(admin.TabularInline):
    model = StartingEquipment
    extra = 1

# ==========================================
# 2. KONFIGURACJA GŁÓWNYCH MODELI
# ==========================================

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'character_class', 'level', 'race', 'user', 'created_at')
    list_filter = ('character_class', 'race', 'level')
    search_fields = ('character_name', 'user__username')
    # Tu podpinamy te "dzieci", żeby edytować je w jednym miejscu
    inlines = [InventoryItemInline, CharacterSkillProficiencyInline]

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'skill_choices_count')
    inlines = [SubclassInline, StartingEquipmentInline, ClassSpellInline]

@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'school', 'casting_time', 'ritual', 'concentration')
    list_filter = ('level', 'school', 'ritual', 'concentration')
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'weight')
    search_fields = ('name',)

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'feature_name')

admin.site.register(Feat)
admin.site.register(Skill)
admin.site.register(Tool)
admin.site.register(Language)
admin.site.register(Subclass) 
admin.site.register(RaceModifier)

admin.site.register(ClassSkillChoice)
admin.site.register(BackgroundStartingEquipment)
admin.site.register(BackgroundSkillProficiency)
admin.site.register(BackgroundToolProficiency)