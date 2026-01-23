from django.contrib import admin # type: ignore
from .models import Character, Language, Subclass, CharacterClass

admin.site.register(Character)
# Register your models here.

admin.site.register(Language)
admin.site.register(Subclass)
admin.site.register(CharacterClass)
