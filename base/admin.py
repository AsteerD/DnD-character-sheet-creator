from django.contrib import admin
from .models import Character, Language
from .classes.rogue import Rogue
from .classes.cleric import Cleric


admin.site.register(Character)
admin.site.register(Language)
admin.site.register(Rogue)
admin.site.register(Cleric)