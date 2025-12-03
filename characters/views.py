import random  # Necesario para random.choice y random.random

from django.shortcuts import render, redirect
from .factories import CharacterFactory
from .strategies import (
    WarriorAttack, MageAttack, RogueAttack,
    WarriorSpecial, MageSpecial, RogueSpecial,
    motivation_bonus
)
from .models import Skin


# ---------------------------------------------------
# CREACIÓN DE PERSONAJE
# ---------------------------------------------------
def create_character_view(request):
    # Cuando volvés a elegir personaje, limpiamos la sesión
    request.session.flush()

    character_type = request.GET.get("character_type")

    if character_type:
        factory = CharacterFactory()
        character = factory.create_character(character_type)

        request.session['character_type'] = character_type
        request.session['character_name'] = character.name

        return redirect('vestuario')

    return render(request, "create_character.html")


# ---------------------------------------------------
# VESTUARIO (SELECCIÓN DE SKIN + MOTIVACIÓN)
# ---------------------------------------------------
def vestuario_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")

    if character_type == "mage":
        skins = Skin.objects.filter(name__icontains="Veigar")
    elif character_type == "warrior":
        skins = Skin.objects.filter(name__icontains="Aatrox")
    else:
        skins = Skin.objects.filter(name__icontains="Varus")

    if request.method == "POST":
        # Si vino un skin_id, es que apretó un botón "Elegir" de una skin
        skin_id = request.POST.get("skin_id")
        if skin_id:
            request.session["skin_id"] = skin_id

        # Siempre guardamos motivación si viene en POST
        motivation = request.POST.get("motivation")
        if motivation:
            request.session["motivation"] = motivation
            # Si ya eligió motivación, pasamos a Lore
            return redirect("lore")

    return render(request, "character_vestuario.html", {
        "character_type": character_type,
        "character_name": character_name,
        "skins": skins,
    })


# ---------------------------------------------------
# LORE DINÁMICO
# ---------------------------------------------------
def lore_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")
    motivation = request.session.get("motivation", "Sabiduría")
    skin_id = request.session.get("skin_id")

    if not character_type or not skin_id:
        return redirect("create_character")

    skin = Skin.objects.filter(id=skin_id).first()
    skin_image = f"/static/imagenes/{skin.sprite}" if skin else "/static/imagenes/mago.png"

    # ===== LORE DINÁMICO POR CLASE =====
    base_lore = {
        "mage": [
            f"{character_name} nació como un diminuto error arcano en un mundo que jamás lo tomó en serio.",
            "Pero el olvido y la burla alimentaron una oscuridad que nadie vio venir.",
        ],
        "warrior": [
            f"{character_name} fue una vez un guerrero venerado, un dios caminando entre mortales.",
            "Hasta que la guerra le arrebató un propósito… y dejó solo hambre de destrucción.",
        ],
        "rogue": [
            f"{character_name} fue un arquero cuya precisión podía decidir el destino de un reino.",
            "Pero la venganza ató su alma a la corrupción, y ahora su flecha nunca se detiene.",
        ],
    }

    # ===== TEXTO DE SKIN =====
    skin_lore = {
        "Veigar Clásico": [
            "Aunque pequeño, su ambición es el abismo donde caerán los soberbios.",
            "Cada hechizo que lanza consume una parte del mundo… para alimentar la suya.",
        ],
        "Veigar Jefe Final": [
            "Ya no participa del juego. Él es el error fatal del sistema.",
            "Cuando su risa suena… la realidad colapsa en un Game Over inevitable.",
        ],
        "Aatrox Guerrero": [
            "Sus alas fueron cadenas; su espada, la sentencia de un dios caído.",
            "Con cada golpe reclama algo que el mundo le robó: su divinidad.",
        ],
        "Aatrox Luna Sangre": [
            "El ritual lunar lo volvió una calamidad viviente.",
            "El cielo tiembla cuando su filo se impregna en luz carmesí.",
        ],
        "Varus Arquero": [
            "Tres almas luchan dentro de su pecho, ninguna en paz.",
            "Su flecha no persigue el futuro… lo destruye.",
        ],
        "Varus Proyecto": [
            "Redefinido por algoritmos, su humanidad ya no es más que un error de sistema.",
            "Un arma perfecta sin voluntad; una voluntad perfecta sin alma.",
        ],
    }

    # ===== MOTIVACIÓN (Bloque 4) =====
    motivation_lore = {
        "Venganza": "Solo una cosa le da fuerza: que el mundo sienta cada grito que él sufrió.",
        "Honor": "Aunque su sendero sea de sangre, cree ser el único capaz de corregir el destino.",
        "Gloria": "Desea que su nombre sobreviva incluso si el universo debe morir para recordarlo.",
        "Sabiduría": "Conoce verdades prohibidas… y usará ese conocimiento sin importarle el costo.",
    }

    # ===== FINAL =====
    final_lines = {
        "mage": "Lo diminuto ya no teme; ahora es la oscuridad la que teme volverse diminuta ante él.",
        "warrior": "Quien intente detenerlo solo acelerará la llegada del último amanecer.",
        "rogue": "Cuando la flecha parte, el destino ya está muerto.",
    }

    # Obtener los bloques correctos
    blocks = []
    blocks.extend(base_lore.get(character_type, []))
    blocks.extend(skin_lore.get(skin.name, []))
    blocks.append(motivation_lore.get(motivation, ""))
    blocks.append(final_lines.get(character_type, ""))

    # Limpiar líneas vacías
    lore_lines = [line.strip() for line in blocks if line.strip()]

    return render(request, "lore.html", {
        "character_name": character_name,
        "skin_image": skin_image,
        "lore_lines": lore_lines,
    })



# ---------------------------------------------------
# BATALLA (con energía + enemigo aleatorio)
# ---------------------------------------------------
# ---------------------------------------------------
# BATALLA (con energía + enemigo aleatorio)
# ---------------------------------------------------
def battle_view(request):
    character_type = request.session.get("character_type")
    character_name = request.session.get("character_name")
    motivation = request.session.get("motivation", "Sabiduría")
    skin_id = request.session.get("skin_id")

    if not character_type:
        return redirect("create_character")

    skin = Skin.objects.filter(id=skin_id).first()
    player_sprite = skin.sprite if skin else "mago.png"

    enemies = {
        "mage": ["warrior", "rogue"],
        "warrior": ["mage", "rogue"],
        "rogue": ["mage", "warrior"],
    }

    enemy_data = {
        "mage": ("Veigar", "mago.png"),
        "warrior": ("Aatrox", "guerrero.png"),
        "rogue": ("Varus", "arquero.png"),
    }

    if "enemy_type" not in request.session:
        request.session["enemy_type"] = random.choice(enemies[character_type])

    enemy_type = request.session["enemy_type"]
    enemy_name, enemy_sprite = enemy_data[enemy_type]

    stats = {
        "mage": {"hp": 100, "atk": 22},
        "warrior": {"hp": 120, "atk": 25},
        "rogue": {"hp": 90, "atk": 20},
    }

    enemy_hp_init = 95
    player_hp_init = stats[character_type]["hp"]
    energy_init = 100

    if request.method == "GET":
        request.session["enemy_hp"] = enemy_hp_init
        request.session["player_hp"] = player_hp_init
        request.session["player_energy"] = energy_init
        request.session["enemy_energy"] = energy_init

    enemy_hp = request.session.get("enemy_hp", enemy_hp_init)
    player_hp = request.session.get("player_hp", player_hp_init)
    player_energy = request.session.get("player_energy", energy_init)
    enemy_energy = request.session.get("enemy_energy", energy_init)

    if character_type == "warrior":
        normal, special = WarriorAttack(), WarriorSpecial()
    elif character_type == "mage":
        normal, special = MageAttack(), MageSpecial()
    else:
        normal, special = RogueAttack(), RogueSpecial()

    battle_text = ""

    # === FRASES OSCURAS por clase enemigo ===
    enemy_quotes = {
        "mage": [
            "La oscuridad ríe contigo... o de ti.",
            "Tu destino es un glitch en mi código.",
            "La realidad ya no te pertenece.",
        ],
        "warrior": [
            "El fin es mi único aliado.",
            "Tu sangre es la firma del final.",
            "Destruiré tu esperanza como he destruido todo.",
        ],
        "rogue": [
            "Nadie escapa de su propio final.",
            "El destino escribió tu nombre en mi flecha.",
            "Tres almas… una decisión: tu muerte.",
        ],
    }

    if request.method == "POST":
        action = request.POST.get("action")

        # --------- TURNO DEL JUGADOR ----------
        if action == "attack":
            result = normal.attack()
            dmg = result["damage"] + motivation_bonus(motivation)
            enemy_hp -= dmg
            player_energy = min(player_energy + 10, 100)
            battle_text += f"{character_name} usa {result['name']} causando {dmg} de daño."
            if result.get("critical"):
                battle_text += " 💥 <span class='crit'>¡GOLPE CRÍTICO!</span> 💥"

        elif action == "special":
            if player_energy >= 40:
                result = special.attack()
                dmg = result["damage"] + motivation_bonus(motivation)
                enemy_hp -= dmg
                player_energy -= 40
                battle_text += f"{character_name} desata {result['name']} causando {dmg} de daño."
                if result.get("critical_forced"):
                    battle_text += " 💥 <span class='crit'>¡PODER DESATADO!</span> 💥"
            else:
                battle_text += f"{character_name} intenta usar su poder, pero no tiene energía.<br>"

        else:
            battle_text += f"{character_name} adopta postura defensiva."
            player_energy = min(player_energy + 20, 100)

        enemy_hp = max(enemy_hp, 0)
        request.session["enemy_hp"] = enemy_hp
        request.session["player_energy"] = player_energy

        if enemy_hp > 0:
            # --------- TURNO DEL ENEMIGO ----------
            enemy_action = "attack"
            if enemy_energy >= 40 and random.random() < 0.35:
                enemy_action = "special"

            if enemy_action == "special":
                enemy_base_damage = 35
                text_name = "Técnica Devastadora"
                enemy_energy -= 40
            else:
                enemy_base_damage = 20
                text_name = "Ataque Feroz"

                if random.random() < 0.20:
                    enemy_base_damage *= 2
                    battle_text += "<br><span class='crit'>¡El enemigo realiza un golpe crítico!</span>"

            if action == "defend":
                enemy_base_damage = int(enemy_base_damage * 0.5)

            player_hp -= enemy_base_damage
            player_hp = max(player_hp, 0)
            enemy_energy = min(enemy_energy + 10, 100)

            battle_text += f"<br>El enemigo {enemy_name} usa {text_name} y te hace {enemy_base_damage} de daño."

            # 👇 FRASE OSCURA
            battle_text += f"<br><em>{random.choice(enemy_quotes.get(enemy_type, []))}</em>"

            request.session["player_hp"] = player_hp
            request.session["enemy_energy"] = enemy_energy

    # ¿Terminó la batalla?
    finished = enemy_hp <= 0 or player_hp <= 0
    if enemy_hp <= 0:
        result = "GLORIA EN LAS CENIZAS"
    elif player_hp <= 0:
        result = "EL ABISMO TE HA RECLAMADO"
    else:
        result = ""

    return render(request, "batalla.html", {
        "character_name": character_name,
        "character_type": character_type,
        "enemy_name": enemy_name,
        "battle_text": battle_text,
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "player_energy": player_energy,
        "enemy_energy": enemy_energy,
        "finished": finished,
        "result": result,
        "player_sprite": player_sprite,
        "enemy_sprite": enemy_sprite,
    })
# ---------------------------------------------------