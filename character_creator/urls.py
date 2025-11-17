from django.contrib import admin
from django.urls import path
from characters.views import battle_view, create_character_view,lore_view, vestuario_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', create_character_view, name='create_character'),
    path('vestuario/', vestuario_view, name='vestuario'),
    path('lore/', lore_view, name="lore"),
    path('batalla/', battle_view, name="batalla"),
]