from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    
    path('', views.CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', views.CharacterDetail.as_view(), name='character'),
    path('character-create/', views.CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', views.CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', views.CharacterDelete.as_view(), name='character-delete'),
    
    path('character/<int:pk>/spells/', views.character_spells, name='character_spells'),
    
    # AJAX Paths
    path('ajax/subclasses/', views.subclasses_for_class, name='subclasses_for_class'),
    path('skills-for-class/', views.skills_for_class, name='skills_for_class'),
]