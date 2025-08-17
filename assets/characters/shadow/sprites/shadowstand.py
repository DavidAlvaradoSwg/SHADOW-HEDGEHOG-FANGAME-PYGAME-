# shadowstand.py
import pygame

# --- Dimensiones del personaje ---
SHADOW_WIDTH = 40
SHADOW_HEIGHT = 60
SHADOW_COLOR = (0, 0, 0) # Negro

# --- Posición inicial del personaje ---
shadow_x = SCREEN_WIDTH // 4 # Un cuarto de la pantalla desde la izquierda
shadow_y = SCREEN_HEIGHT - 150 # Un poco por encima del suelo

def draw_shadow(screen, x, y):
    pygame.draw.rect(screen, SHADOW_COLOR, (x, y, SHADOW_WIDTH, SHADOW_HEIGHT))

# --- Integración en el bucle principal (ejemplo) ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235)) # Fondo de prueba
    draw_background(screen) # Dibujar nuestro fondo de código
    draw_shadow(screen, shadow_x, shadow_y) # Dibujar a Shadow
    pygame.display.flip()

pygame.quit()