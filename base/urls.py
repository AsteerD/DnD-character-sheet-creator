from django.urls import path
from .views import (
    CharacterList,
    CharacterDetail,
    CharacterCreate,
    CharacterUpdate,
    CharacterDelete,
    CustomLoginView,
    RegisterPage
)

urlpatterns = [
    path('', CharacterList.as_view(), name='characters'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character/<int:pk>/edit/', CharacterUpdate.as_view(), name='character-update'),
    path('character/<int:pk>/delete/', CharacterDelete.as_view(), name='character-delete'),
]
