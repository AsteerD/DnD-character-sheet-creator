from django.urls import path
from .views import CharacterCreateView

urlpatterns = [
    path('characters/', CharacterCreateView.as_view(), name='api-create-character'),
]
