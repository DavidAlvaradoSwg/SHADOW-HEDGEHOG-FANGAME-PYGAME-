# test_minimal.py
import sys

print("Paso 1: Iniciando el script de prueba.")

try:
    from levels import LEVEL_DATA
    print("Paso 2: 'levels.py' importado correctamente.")
    from background import ProceduralBackground
    print("Paso 3: 'background.py' importado correctamente.")
    import pygame
    print("Paso 4: Pygame importado correctamente.")
except Exception as e:
    print("\n" + "="*60)
    print("¡ERROR FATAL DURANTE LA IMPORTACIÓN!")
    print("El programa no puede empezar. Revisa el error de abajo.")
    print(f"Error detallado: {e}")
    print("Posibles causas:")
    print("- Hay un error de sintaxis en 'levels.py' o 'background.py'.")
    print("- Los archivos no están en la misma carpeta.")
    print("- Pygame no está instalado correctamente.")
    print("="*60)
    input("Presiona Enter para salir...")  # Mantiene la ventana abierta
    sys.exit()

print("\nTodos los archivos se importaron sin problemas.")
print("Intentando inicializar Pygame y crear el fondo...")

try:
    pygame.init()
    screen = pygame.display.set_mode((100, 100))  # Pantalla de prueba
    LEVEL_TO_TEST = "forest_zone"
    background = ProceduralBackground(screen, LEVEL_TO_TEST)
    print("\n" + "="*60)
    print("¡ÉXITO! El fondo se ha creado sin errores.")
    print("Esto significa que 'levels.py' y 'background.py' funcionan.")
    print("El problema debe estar en el bucle principal de tu juego principal.")
    print("="*60)
except Exception as e:
    print("\n" + "="*60)
    print("¡ERROR AL CREAR EL OBJETO DE FONDO!")
    print("El problema ocurrió al intentar crear la clase 'ProceduralBackground'.")
    print(f"Error detallado: {e}")
    print(f"Revisa los datos para el nivel '{LEVEL_TO_TEST}' en tu archivo 'levels.py'.")
    print("="*60)
finally:
    pygame.quit()
    input("Presiona Enter para salir...")  # Mantiene la ventana abierta
    sys.exit()