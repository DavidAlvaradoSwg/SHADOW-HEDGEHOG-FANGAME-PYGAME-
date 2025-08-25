# test_background.py
import pygame
import sys

# --- CONFIGURACIÓN BÁSICA ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# --- Puedes cambiar esto a "desert_zone" o "cityspace_zone" para probar otros niveles ---
LEVEL_TO_TEST = "forest_zone" 

# --- IMPORTACIÓN CON MANEJO DE ERRORES ---
# Este bloque nos dirá si el problema está en la sintaxis de tus archivos.
try:
    from levels import LEVEL_DATA
    from background import ProceduralBackground
except ImportError as e:
    print("="*60)
    print("¡ERROR DE IMPORTACIÓN! ¿Están los archivos en la misma carpeta?")
    print(f"No se pudo importar 'levels' o 'background'. Asegúrate de que los archivos")
    print("'levels.py' y 'background.py' existen en la misma carpeta que este script.")
    print(f"Error detallado: {e}")
    print("="*60)
    sys.exit()
except Exception as e:
    print("="*60)
    print("¡ERROR DE SINTAXIS EN EL ARCHIVO levels.py!")
    print("Parece que hay un error de sintaxis en tu archivo 'levels.py'.")
    print("Revisa que todos los diccionarios, listas, comas y paréntesis estén correctos.")
    print(f"Error detallado: {e}")
    print("="*60)
    sys.exit()


# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Test de Fondo - Nivel: {LEVEL_TO_TEST}")
clock = pygame.time.Clock()

# --- CREACIÓN DEL FONDO ---
try:
    background = ProceduralBackground(screen, LEVEL_TO_TEST)
except Exception as e:
    print("="*60)
    print("¡ERROR AL CREAR EL OBJETO ProceduralBackground!")
    print(f"El problema ocurrió durante la inicialización (__init__) de la clase.")
    print(f"Revisa que el nivel '{LEVEL_TO_TEST}' exista en tu archivo levels.py.")
    print(f"Error detallado: {e}")
    print("="*60)
    pygame.quit()
    sys.exit()

print("\n¡El script de prueba se ha iniciado correctamente!")
print("Usa las flechas IZQUIERDA y DERECHA para mover el fondo.")
print("Presiona ESC para salir.")

# --- BUCLE PRINCIPAL DE PRUEBA ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Simular movimiento del jugador
    keys = pygame.key.get_pressed()
    scroll_delta = 0
    if keys[pygame.K_RIGHT]:
        scroll_delta = -5 # El mundo se mueve a la izquierda
    if keys[pygame.K_LEFT]:
        scroll_delta = 5  # El mundo se mueve a la derecha

    # --- Actualización ---
    background.update(scroll_delta)

    # --- Dibujado ---
    # La pantalla se limpia dentro de background.draw() con la capa "solid_color"
    background.draw()

    # --- Actualizar pantalla ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
