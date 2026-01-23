from django.urls import path
from .views import (
    CharacterList, 
    CharacterDetail, 
    CharacterCreate, 
    CharacterUpdate, 
    CharacterDelete, 
    CustomLoginView, 
    RegisterPage,
    ajax_load_subclasses
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),

    # AJAX URL (musi pasować do tego w pliku HTML i views.py)
    path('ajax/load-subclasses/', ajax_load_subclasses, name='ajax_load_subclasses'),
]