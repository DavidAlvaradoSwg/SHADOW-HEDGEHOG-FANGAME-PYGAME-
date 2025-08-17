# main.py
import pygame
import os
import random
import math
import time

from maps.forest_zone import ForestZone

# --- Directorio base del proyecto ---
# Esto nos asegura que las rutas a los assets funcionen sin importar desde dónde se ejecute el script.
_project_root = os.path.dirname(os.path.abspath(__file__))

# --- Configuración de la pantalla ---
BASE_WIDTH = 800
BASE_HEIGHT = 600

# Calcular el nuevo tamaño de la ventana según las especificaciones
SCREEN_WIDTH = int(BASE_WIDTH * 1.75)
SCREEN_HEIGHT = int(BASE_HEIGHT * 1.5)

# --- Inicialización de Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow the Hedgehog")

# --- Colores ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (200, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 200)

# --- Fuentes para el texto ---
title_font = pygame.font.SysFont('Arial', 72, bold=True)
subtitle_font = pygame.font.SysFont('Arial', 36)

# --- Funciones auxiliares ---
def lerp_color(color1, color2, t):
    """Interpola linealmente entre dos colores."""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

# --- Clases de la escena ---
class Star:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed = random.uniform(0.5, 2.0)
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 1)

class TitleScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = [Star(screen_width, screen_height) for _ in range(200)]  # Más estrellas para un efecto de galaxia
        
        # Cargar la imagen del personaje Shadow
        try:
            # Ruta simplificada. Asegúrate de que el archivo 'shadow.png' esté en 'assets/characters/'
            shadow_path = os.path.join(_project_root, "assets", "characters", "shadow.png")
            print(f"Intentando cargar la imagen de Shadow desde: {shadow_path}")
            self.shadow_image = pygame.image.load(shadow_path).convert_alpha()
            self.shadow_image = pygame.transform.scale(self.shadow_image, (250, 250)) # Hacemos la imagen un poco más grande
        except pygame.error as e:
            print("************************************************************")
            print(f"¡ERROR! No se pudo cargar la imagen de Shadow: {e}")
            print(f"Asegúrate de que el archivo '{os.path.abspath(shadow_path)}' exista.")
            print("El juego continuará sin la imagen del personaje.")
            print("************************************************************")
            self.shadow_image = None

        # Configuración para la animación del círculo
        self.circle_colors = [RED, PURPLE, BLUE, GOLD]
        self.color_change_speed = 0.4
        self.start_time = time.time()

        # Estrellas dentro del círculo
        self.inner_stars = []
        circle_radius = 200
        circle_center_x = screen_width // 2
        circle_center_y = screen_height // 2
        for _ in range(70):
            angle = random.uniform(0, 2 * math.pi)
            # Usamos una raíz cuadrada para que las estrellas no se agrupen en el centro
            radius = math.sqrt(random.uniform(0, 1)) * (circle_radius - 10)
            star_x = circle_center_x + radius * math.cos(angle)
            star_y = circle_center_y + radius * math.sin(angle)
            star_alpha = random.randint(50, 200)
            star_alpha_direction = random.choice([-1, 1])
            self.inner_stars.append([star_x, star_y, star_alpha, star_alpha_direction])
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Dibujar estrellas de fondo
        for star in self.stars:
            star.move()
            star.draw(self.screen)
        
        # --- Animación de Color del Círculo ---
        time_elapsed = time.time() - self.start_time
        t = (time_elapsed * self.color_change_speed) % len(self.circle_colors)
        color_index1 = int(t)
        color_index2 = (color_index1 + 1) % len(self.circle_colors)
        lerp_t = t - color_index1
        
        current_border_color = lerp_color(
            self.circle_colors[color_index1],
            self.circle_colors[color_index2],
            lerp_t
        )

        # Dibujar el círculo central
        circle_radius = 200
        circle_x = self.screen_width // 2
        circle_y = self.screen_height // 2
        pygame.draw.circle(self.screen, current_border_color, (circle_x, circle_y), circle_radius + 5, 5) # Borde con color animado
        pygame.draw.circle(self.screen, BLACK, (circle_x, circle_y), circle_radius)

        # Dibujar estrellas parpadeantes dentro del círculo
        for star in self.inner_stars:
            # Animar el parpadeo (alpha)
            star[2] += 5 * star[3]
            if not 50 <= star[2] <= 200:
                star[3] *= -1
                star[2] = max(50, min(200, star[2]))
            star_color = (star[2], star[2], star[2])
            pygame.draw.circle(self.screen, star_color, (int(star[0]), int(star[1])), 1)

        # Colocar la imagen de Shadow en el centro del círculo
        if self.shadow_image:
            shadow_rect = self.shadow_image.get_rect(center=(circle_x, circle_y))
            self.screen.blit(self.shadow_image, shadow_rect)
        
        # Textos con un estilo más definido
        title_text = title_font.render("SHADOW THE HEDGEHOG", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 250))
        self.screen.blit(title_text, title_rect)
        
        creator_text = subtitle_font.render("FanGame created by JDSA", True, WHITE)
        creator_rect = creator_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 250))
        self.screen.blit(creator_text, creator_rect)

        press_start_text = subtitle_font.render("Press Enter", True, GOLD)
        press_start_rect = press_start_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(press_start_text, press_start_rect)
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return "main_menu"
        return None

class MainMenuScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_options = ["SELECT MAP", "SCORE", "QUIT"]
        self.selected_option = 0
        self.option_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.selected_color = GOLD
        self.default_color = WHITE
        self.stars = [Star(screen_width, screen_height) for _ in range(200)]

    def draw(self):
        self.screen.fill(BLACK)
        for star in self.stars:
            star.move()
            star.draw(self.screen)
        
        title_text = title_font.render("MAIN MENU", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.menu_options):
            color = self.selected_color if i == self.selected_option else self.default_color
            text = self.option_font.render(option, True, color)
            rect = text.get_rect(center=(self.screen_width // 2, 300 + i * 80))
            self.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.selected_option == 0: # SELECT MAP
                    return "map_select"
                elif self.selected_option == 1: # SCORE
                    return "score"
                elif self.selected_option == 2: # QUIT
                    return "quit"
        return None

class MapSelectionScreen:
    """Pantalla para seleccionar un mapa de juego."""
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        # En el futuro, podrías cargar estos desde un directorio
        self.maps = ["FOREST ZONE"] 
        self.selected_map_index = 0
        self.map_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.selected_color = GOLD
        self.default_color = WHITE
        self.stars = [Star(screen_width, screen_height) for _ in range(100)]
        
        self.map_previews = {}
        self._load_previews()

    def _load_previews(self):
        """Carga las imágenes de vista previa para cada mapa."""
        for map_name in self.maps:
            map_key = map_name.replace(" ", "_").lower()
            # Intenta cargar .jpg y luego .png
            for ext in ["jpg", "png"]:
                preview_path = os.path.join(_project_root, "assets", "previews", f"{map_key}_preview.{ext}")
                try:
                    image = pygame.image.load(preview_path).convert()
                    self.map_previews[map_name] = pygame.transform.scale(image, (600, 338))
                    print(f"Loaded preview: {preview_path}")
                    break
                except pygame.error:
                    continue
            else:
                print(f"Warning: Preview for {map_name} not found. Using fallback surface.")
                fallback_surface = pygame.Surface((600, 338))
                fallback_surface.fill(PURPLE)
                self.map_previews[map_name] = fallback_surface

    def draw(self):
        self.screen.fill(BLACK)
        for star in self.stars:
            star.move()
            star.draw(self.screen)

        title_text = title_font.render("SELECT A MAP", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Dibuja la vista previa del mapa seleccionado
        selected_map_name = self.maps[self.selected_map_index]
        preview_image = self.map_previews.get(selected_map_name)
        if preview_image:
            preview_rect = preview_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
            self.screen.blit(preview_image, preview_rect)

        # Dibuja el nombre del mapa seleccionado
        # (Podrías añadir flechas si tuvieras más de un mapa)
        map_text = self.map_font.render(selected_map_name, True, self.selected_color)
        map_rect = map_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 200))
        self.screen.blit(map_text, map_rect)

        # Instrucciones
        info_text = subtitle_font.render("Press Enter to Start", True, WHITE)
        info_rect = info_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        self.screen.blit(info_text, info_rect)
        
        esc_text = subtitle_font.render("Press ESC to go back", True, WHITE)
        esc_rect = esc_text.get_rect(center=(self.screen_width // 2, self.screen_height - 60))
        self.screen.blit(esc_text, esc_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_map_index = (self.selected_map_index - 1) % len(self.maps)
            elif event.key == pygame.K_RIGHT:
                self.selected_map_index = (self.selected_map_index + 1) % len(self.maps)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                selected_map_name = self.maps[self.selected_map_index]
                # Devuelve una tupla para indicar que se inicie el juego con un mapa específico
                return ("start_game", selected_map_name)
            elif event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None

class GameScreen:
    """Pantalla de juego principal donde se desarrolla la acción."""
    def __init__(self, screen, screen_width, screen_height, map_name):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_name = map_name
        self.map_instance = None
        self.current_act = 1
        self.info_font = pygame.font.SysFont('Arial', 24)
        
        self._load_map()

    def _load_map(self):
        """Carga la instancia del mapa basado en el nombre."""
        if self.map_name == "FOREST ZONE":
            self.map_instance = ForestZone(self.screen_width, self.screen_height, _project_root)
        # Aquí podrías añadir 'elif' para otros mapas en el futuro
        else:
            print(f"Error: Mapa '{self.map_name}' no reconocido.")
            # Podrías tener un mapa por defecto o volver al menú
            self.map_instance = None
        
        if self.map_instance:
            self.map_instance.load_act(self.current_act)

    def draw(self):
        if self.map_instance:
            self.map_instance.draw(self.screen)
            
            # Dibuja instrucciones en la pantalla de juego
            instructions = "Use <- -> to change acts | Press ESC to exit"
            info_surf = self.info_font.render(instructions, True, WHITE)
            info_rect = info_surf.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
            self.screen.blit(info_surf, info_rect)
        else:
            # Pantalla de error si el mapa no se pudo cargar
            self.screen.fill(BLACK)
            text = subtitle_font.render(f"Error loading map: {self.map_name}", True, RED)
            rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "map_select" # Volver a la selección de mapa
            elif event.key == pygame.K_LEFT:
                self.current_act = max(1, self.current_act - 1)
                self.map_instance.load_act(self.current_act)
            elif event.key == pygame.K_RIGHT:
                self.current_act = min(len(self.map_instance.acts), self.current_act + 1)
                self.map_instance.load_act(self.current_act)
        return None


class ScoreScreen:
    """Placeholder for the score screen."""
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self):
        self.screen.fill(BLACK)
        text = subtitle_font.render("Score Screen (Placeholder)", True, WHITE)
        rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, rect)

        info_text = subtitle_font.render("Press ESC to return to menu", True, WHITE)
        info_rect = info_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
        self.screen.blit(info_text, info_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "main_menu"
        return None
        
# --- Bucle principal del juego ---
try:
    scenes = {
        'title': TitleScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT),
        'main_menu': MainMenuScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT),
        'map_select': MapSelectionScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT),
        'score': ScoreScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT),
    }
    current_scene_key = 'title'
    current_scene = scenes[current_scene_key]

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            next_scene_key = current_scene.handle_event(event)
            if next_scene_key:
                # Manejo especial para iniciar el juego
                if isinstance(next_scene_key, tuple) and next_scene_key[0] == 'start_game':
                    map_to_load = next_scene_key[1]
                    # Crea una nueva instancia de la pantalla de juego con el mapa seleccionado
                    current_scene = GameScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, map_to_load)
                    continue

                if next_scene_key == 'quit':
                    running = False
                elif next_scene_key in scenes:
                    current_scene = scenes[next_scene_key]
                else:
                    print(f"Scene '{next_scene_key}' not found!")
                    running = False

        if not running:
            break

        current_scene.draw()
        pygame.display.flip()
        clock.tick(60)

except Exception as e:
    print(f"Ocurrió un error: {e}")
    time.sleep(5) 

# --- Salir de Pygame ---
pygame.quit()