def motivation_bonus(m):
    bonuses = {
        "Venganza": 10,
        "Honor": 5,
        "Gloria": 7,
        "Sabiduría": 3
    }
    return bonuses.get(m, 0)


class AttackStrategy:
    def attack(self):
        raise NotImplementedError


class WarriorAttack(AttackStrategy):
    def attack(self):
        return {
            "name": "Golpe Demoniaco",
            "damage": 25
        }


class MageAttack(AttackStrategy):
    def attack(self):
        return {
            "name": "Explosión Arcana",
            "damage": 22
        }


class RogueAttack(AttackStrategy):
    def attack(self):
        return {
            "name": "Flecha Sombría",
            "damage": 20
        }
