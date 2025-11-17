from django.shortcuts import render, redirect
from .factories import CharacterFactory
from .strategies import WarriorAttack, MageAttack, RogueAttack, motivation_bonus


def create_character_view(request):
    character_type = request.GET.get("character_type")

    if character_type:
        factory = CharacterFactory()
        character = factory.create_character(character_type)

        request.session['character_type'] = character_type
        request.session['character_name'] = character.name

        return redirect('vestuario')

    return render(request, "create_character.html")



def vestuario_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")

    if request.method == "POST":
        motivation = request.POST.get("motivation")
        request.session["motivation"] = motivation
        return redirect("vestuario")

    return render(request, "character_vestuario.html", {
        "character_type": character_type,
        "character_name": character_name
    })



def lore_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")
    motivation = request.session.get("motivation")

    return render(request, "lore.html", {
        "character_type": character_type,
        "character_name": character_name,
        "motivation": motivation
    })



def battle_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")
    motivation = request.session.get("motivation")

    if "enemy_hp" not in request.session:
        request.session["enemy_hp"] = 120
    if "player_hp" not in request.session:
        request.session["player_hp"] = 100

    enemy_hp = request.session["enemy_hp"]
    player_hp = request.session["player_hp"]

    if character_type == "warrior":
        strategy = WarriorAttack()
    elif character_type == "mage":
        strategy = MageAttack()
    else:
        strategy = RogueAttack()

    battle_text = ""

    if request.method == "POST":
        attack_info = strategy.attack()

        base_damage = attack_info["damage"]
        bonus = motivation_bonus(motivation)
        total_damage = base_damage + bonus

        enemy_hp -= total_damage
        request.session["enemy_hp"] = enemy_hp

        battle_text = f"{character_name} usa {attack_info['name']} causando {total_damage} de daño."

        if enemy_hp > 0:
            player_hp -= 15
            request.session["player_hp"] = player_hp
            battle_text += "\nLa Bestia de Sombras contraataca y te hace 15 de daño."

    finished = False
    result = ""

    if enemy_hp <= 0:
        finished = True
        result = "¡Has derrotado a la Bestia de Sombras!"
        request.session["enemy_hp"] = 120
        request.session["player_hp"] = 100

    elif player_hp <= 0:
        finished = True
        result = "Has caído en batalla..."
        request.session["enemy_hp"] = 120
        request.session["player_hp"] = 100

    return render(request, "batalla.html", {
        "character_name": character_name,
        "character_type": character_type,
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "battle_text": battle_text,
        "finished": finished,
        "result": result,
    })
