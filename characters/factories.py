from .models import Character, Skin

class CharacterFactory:
    def create_character(self, character_type):
        defaults = {
            "warrior": ("Aatrox", "Aatrox Original"),
            "mage": ("Veigar", "Veigar Clásico"),
            "rogue": ("Varus", "Varus Original"),
        }

        if character_type not in defaults:
            raise ValueError("Tipo de personaje no reconocido")

        name, default_skin_name = defaults[character_type]
        skin = Skin.objects.filter(name=default_skin_name).first()

        # Stats iniciales — Podés ajustarlos
        if character_type == "warrior":
            strength, magic = 10, 2
        elif character_type == "mage":
            strength, magic = 3, 10
        else:
            strength, magic = 6, 4

        return Character(
            name=name,
            lore="",
            strength=strength,
            magic=magic,
            skin=skin
        )
