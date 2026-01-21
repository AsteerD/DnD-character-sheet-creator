from django.urls import path # pyright: ignore[reportMissingModuleSource]
from .views import (
    CharacterList, 
    CharacterDetail, 
    CharacterCreate, 
    CharacterUpdate, 
    CharacterDelete, 
    CustomLoginView, 
    RegisterPage
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Auth System
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    # Main Character Views
    # This is the 'characters' name that reverse_lazy('characters') in views.py points to
    path('', CharacterList.as_view(), name='characters'),
    
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),
]