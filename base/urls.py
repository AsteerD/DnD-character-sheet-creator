from django.urls import path # pyright: ignore[reportMissingModuleSource]
from .views import CharacterList, CharacterDetail, CharacterCreate, CharacterUpdate, CharacterDelete, CharacterDelete, CustomLoginView, RegisterPage 
from django.contrib.auth.views import LogoutView

from base import views


urlpatterns = [
    path('', CharacterList.as_view(), name='characters'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character/<int:pk>/edit/', CharacterUpdate.as_view(), name='character-update'),
    path('character/<int:pk>/delete/', CharacterDelete.as_view(), name='character-delete'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),
    path("ajax/subclasses/", views.subclasses_for_class, name="subclasses_for_class"),
]
