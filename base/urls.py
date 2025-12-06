from django.urls import path # pyright: ignore[reportMissingModuleSource]
from .views import CharacterList

urlpatterns = [
    path('', CharacterList.as_view(), name='home'),
]