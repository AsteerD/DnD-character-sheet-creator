from django.urls import path # pyright: ignore[reportMissingModuleSource]
from .views import CharacterList, CharacterDetail, CharacterCreate, CharacterUpdate, CharacterDelete, CharacterDelete, character_spells, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # --- AUTHENTICATION ---
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # --- CHARACTER ---
    path('', CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character/<int:pk>/edit/', CharacterUpdate.as_view(), name='character-update'),
    path('character/<int:pk>/delete/', CharacterDelete.as_view(), name='character-delete'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),
    path('character/<int:pk>/spells/', character_spells, name='character_spells'),

]

