# player.py
import pygame

# --- Dimensiones del personaje ---
SHADOW_WIDTH = 40
SHADOW_HEIGHT = 60
SHADOW_COLOR = (0, 0, 0) # Negro para su cuerpo
HAIR_COLOR = (255, 0, 0) # Rojo para el pelo

def draw_shadow(screen, x, y):
    # Cuerpo principal (forma ovalada)
    body_rect = pygame.Rect(x, y, SHADOW_WIDTH, SHADOW_HEIGHT)
    pygame.draw.ellipse(screen, SHADOW_COLOR, body_rect)

    # Ojos y boca (simples para empezar)
    eye_color = (255, 255, 255) # Blanco
    pupil_color = (0, 0, 0) # Negro
    pygame.draw.circle(screen, eye_color, (x + 15, y + 20), 5)
    pygame.draw.circle(screen, pupil_color, (x + 16, y + 20), 2)
    pygame.draw.circle(screen, eye_color, (x + 25, y + 20), 5)
    pygame.draw.circle(screen, pupil_color, (x + 26, y + 20), 2)
    
    # Nariz (ejemplo simple)
    pygame.draw.circle(screen, (255, 128, 0), (x + 20, y + 25), 3)

    # Pelos (espinas rojas y negras)
    # Espina de arriba (roja)
    spine_points = [(x + 20, y - 5), (x + 10, y + 10), (x + 30, y + 10)]
    pygame.draw.polygon(screen, HAIR_COLOR, spine_points)
    
    # Espina de abajo (negra)
    spine_points2 = [(x + 20, y + 5), (x + 15, y + 15), (x + 25, y + 15)]
    pygame.draw.polygon(screen, SHADOW_COLOR, spine_points2)


# --- Integración en el bucle principal ---
# (Puedes usar esto dentro del bucle de tu main.py para verlo)
running = True
while running:
    # ... (manejo de eventos) ...
    screen.fill((0, 0, 0)) # Limpiar la pantalla
    draw_shadow(screen, 380, 280) # Dibujar a Shadow en el centro
    pygame.display.flip()
# --- Ejemplo de lógica en main.py ---
# Supongamos que level.py tiene un método load_act(act_number)
current_act = 1

# ... dentro del bucle del juego
# Lógica para cuando el jugador muere
if player.is_dead():
    player.lives -= 1
    if player.lives > 0:
        current_act = 1
        level.load_act(current_act)
    else:
        game_state = "GAME_OVER"