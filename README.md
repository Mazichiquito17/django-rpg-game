# 🛡️ DARK FANTASY CHARACTER CREATOR — Django + Docker 🐳

Proyecto desarrollado como parte de la materia de programación web / backend.
Aplicación web estilo RPG donde el usuario crea un héroe, elige su skin,
motivo, lee su lore dinámico y enfrenta una batalla final.

---

## 🎮 Características

- Creación de personaje por clases: Guerrero, Mago y Pícaro
- Selección de Skins (Aatrox, Veigar, Varus)
- Lore dinámico según motivación del personaje
- Sistema de combate por turnos:
  - HP, Energía, golpes críticos
  - Acciones: Ataque, Habilidad Especial, Defender
  - Enemigo con IA básica
- Animaciones visuales y efectos
- Proyecto completamente dockerizado ⚙️🐳

---

## 🏗️ Tecnologías Utilizadas

| Tecnología | Uso |
|-----------|-----|
| Django 5.2 | Backend y rutas |
| HTML / CSS | Frontend estilizado (Dark Souls style) |
| Docker | Contenerización de la app |
| Python 3.10 | Lenguaje principal |
| SQLite | Base de datos por defecto |

---

## 🐳 Correr la app con Docker

📌 Requisitos previos:
- Docker Desktop instalado y en ejecución

### ▶️ Construir imagen

```bash
docker build -t juego-dark-souls .

▶️ Ejecutar contenedor
docker run -p 8000:8000 juego-dark-souls

Luego acceder desde el navegador a:
👉 http://localhost:8000

character_creator/
│ manage.py
│ requirements.txt
│ Dockerfile
│ db.sqlite3
├── character_creator/  # Proyecto Django (settings, wsgi, urls)
├── characters/         # App principal con juego
│   ├── templates/      # HTML (views del juego)
│   ├── static/         # Assets (imágenes)
│   ├── views.py        # Lógica de juego
│   ├── models.py
│   ├── strategies.py
│   ├── factories.py
 Autor

Maxi — Estudiante de Desarrollo de Software

Apasionado por programación, videojuegos, y tecnología

¡Objetivo profesional: Trabajar en el mundo del software! 🚀