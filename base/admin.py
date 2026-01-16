from django.contrib import admin
from .models import Character, Rogue, Language # dodaj Rogue tutaj

admin.site.register(Character)
admin.site.register(Language)
admin.site.register(Rogue) # to sprawi, że Rogue pojawi się w panelu