import random

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
        damage = 25
        critical = random.random() < 0.20  # 20% de crítico
        if critical:
            damage *= 2
        return {
            "name": "Golpe Demoniaco",
            "damage": damage,
            "critical": critical
        }


class MageAttack(AttackStrategy):
    def attack(self):
        damage = 22
        critical = random.random() < 0.25
        if critical:
            damage *= 2
        return {
            "name": "Explosión Arcana",
            "damage": damage,
            "critical": critical
        }


class RogueAttack(AttackStrategy):
    def attack(self):
        damage = 20
        critical = random.random() < 0.30
        if critical:
            damage *= 2
        return {
            "name": "Flecha Sombría",
            "damage": damage,
            "critical": critical
        }

class WarriorSpecial:
    def attack(self):
        return {
            "name": "Aplastamiento Infernal",
            "damage": 50,
        }


class MageSpecial:
    def attack(self):
        return {
            "name": "Rayo del Vacío",
            "damage": 35,
            "critical_forced": True  # crítico garantizado
        }


class RogueSpecial:
    def attack(self):
        return {
            "name": "Flecha Fantasmal",
            "damage": 28,
            "ignore_defense": True
        }
