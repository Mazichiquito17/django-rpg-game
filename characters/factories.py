from .models import Character

class CharacterFactory:
    def create_character(self, character_type):
        if character_type == "warrior":
            return Character(name="Aatrox", lore="Un demonio caído que busca redención en la guerra eterna.", strength=10, magic=2)
        elif character_type == "mage":
            return Character(name="Veigar", lore="Un hechicero oscuro obsesionado con el poder y el control del vacío.", strength=3, magic=10)
        elif character_type == "rogue":
            return Character(name="Varus", lore="Un arquero consumido por la venganza, atrapado entre la luz y la oscuridad.", strength=6, magic=4)
        else:
            raise ValueError("Tipo de personaje no reconocido")
