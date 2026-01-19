from django.contrib import admin # type: ignore
from .models import Character, Language

admin.site.register(Character)
# Register your models here.

admin.site.register(Language)

from django.contrib import admin
from .models import Item, InventoryItem  

admin.site.register(Item)
admin.site.register(InventoryItem)