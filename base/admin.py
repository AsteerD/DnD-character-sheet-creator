from django.contrib import admin
from .models import Character, Rogue, Language

admin.site.register(Character)
admin.site.register(Language)
admin.site.register(Rogue)