from django.urls import path # pyright: ignore[reportMissingModuleSource]
from .views import CharacterList, CharacterDetail, CharacterCreate, CharacterUpdate, CharacterDelete, CustomLoginView, RegisterPage, CharacterCreateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    
    #HTML Pages
    path('', CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character/<int:pk>/edit/', CharacterUpdate.as_view(), name='character-update'),
    path('character/<int:pk>/delete/', CharacterDelete.as_view(), name='character-delete'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),

    #Api
    path("characters/", CharacterCreateView.as_view(), name="create-character"),
]
