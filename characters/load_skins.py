from .models import Skin

def load_default_skins():
    skins_data = [
        {
            "name": "Veigar Clásico",
            "image": "mago.png",
            "lore": "La forma original del Maestro del Vacío."
        },
        {
            "name": "Veigar Jefe Final",
            "image": "veigar_jefe_final.png",
            "lore": "Encarnación máxima del caos digital, programado para conquistar cada mundo."
        },
        {
            "name": "Aatrox Original",
            "image": "guerrero.png",
            "lore": "La Espada Darkin en su forma clásica."
        },
        {
            "name": "Aatrox Luna de Sangre",
            "image": "aatrox_luna_sangre.png",
            "lore": "Cuando la luna se tiñe de rojo, nada puede detenerlo."
        },
        {
            "name": "Varus Original",
            "image": "arquero.png",
            "lore": "El arquero oscuro en su forma tradicional."
        },
        {
            "name": "Varus Proyecto",
            "image": "varus_proyecto.png",
            "lore": "Un arma viviente diseñada para eliminar amenazas antes de que existan."
        }
    ]

    for skin in skins_data:
        Skin.objects.get_or_create(**skin)

    print("✔ Skins cargadas correctamente")
