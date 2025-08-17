# title.py
import pygame
import random
import time
import math
import os


# --- Colores ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
SHADOW_DARK = (20, 20, 20)
SKIN_LIGHT = (255, 220, 180)
HAIR_RED = (200, 0, 0)
HAIR_ORANGE = (255, 100, 0)
EYE_WHITE = (255, 255, 255)
EYE_RED = (200, 0, 0)
GOLD = (255, 215, 0)
HAIR_WHITE_HIGHLIGHT = (255, 255, 255)
HAIR_BRIGHT_RED = (255, 50, 50)
GLOVE_SHOE_CUFF_RED = (220, 0, 0)
GLOVE_SHOE_CUFF_BORDER = BLACK


# --- Colores para la animación del círculo ---
CIRCLE_COLORS = [
    (100, 0, 200),
    (200, 0, 50),
    (255, 215, 0),
]


# --- Funciones de Dibujo (GLOBALES) ---


    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=center_pos)
    surface.blit(text_surf, text_rect)

    if reflection:
        reflection_surface = pygame.transform.flip(text_surf, False, True)
        reflection_surface.set_alpha(100)
        reflection_rect = reflection_surface.get_rect(midtop=text_rect.midbottom)
        surface.blit(reflection_surface, reflection_rect)

def draw_star(surface, center, outer_radius, inner_radius, color):
    points = []
    angle_offset = -math.pi / 2

    for i in range(10):
        angle = i * (math.pi / 5) + angle_offset
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)


def lerp_color(color1, color2, t):
    r = int(color1.r + (color2.r - color1.r) * t)
    g = int(color1.g + (color2.g - color1.g) * t)
    b = int(color1.b + (color2.b - color1.b) * t)
    return pygame.Color(r, g, b)

# --- Funciones de Dibujo (ACTUALIZADAS) ---

class TitleScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_time = time.time()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(project_root, "assets", "fonts", "shadow_font.ttf")
        try:
            self.title_font = pygame.font.Font(font_path, 40)
            self.big_title_font = pygame.font.Font(font_path, 95)
            self.subtitle_font = pygame.font.Font(font_path, 42)
        except (FileNotFoundError, pygame.error) as e:
            print("--- ¡ERROR DE CARGA DE FUENTE! ---")
            print(f"No se pudo cargar la fuente desde: {font_path}")
            print(f"Error específico: {e}")
            print("Asegúrate de que la ruta es correcta y el archivo no está corrupto. Usando fuente predeterminada.")
            self.title_font = pygame.font.SysFont("Arial", 40)
            self.big_title_font = pygame.font.SysFont("Arial", 95)
            self.subtitle_font = pygame.font.SysFont("Arial", 42)

        self.stars = self.create_stars()
        self.circle_colors = [pygame.Color(100, 0, 200), pygame.Color(200, 0, 50), pygame.Color(255, 215, 0), pygame.Color(200, 0, 50)]

    def create_stars(self):
        stars_list = []
        for _ in range(100):
            stars_list.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'radius': random.randint(1, 3),
                'alpha': random.randint(50, 200),
                'direction': 1
            })
        return stars_list

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return "MAIN_MENU"
        return

    def draw(self):
        self.screen.fill(BLACK)

        # --- Animación de Estrellas ---
        for star in self.stars:
            star['y'] += 0.5 # Mover estrellas hacia abajo
            if star['y'] > self.screen_height:
                star['y'] = 0
                star['x'] = random.randint(0, self.screen_width)

            # Efecto de pulso en el brillo
            star['alpha'] += 5 * star['direction']
            if not 50 <= star['alpha'] <= 200:
                star['direction'] *= -1
                star['alpha'] = max(50, min(200, star['alpha']))

            star_color = (star['alpha'], star['alpha'], star['alpha'])
            pygame.draw.circle(self.screen, star_color, (star['x'], star['y']), star['radius'])

        # --- Animación de Color del Círculo ---
        current_time = time.time()
        color_change_speed = 0.5
        t = (math.sin(current_time * color_change_speed) + 1) / 2
        color_index = int(t * (len(self.circle_colors) - 1))
        next_color_index = (color_index + 1) % len(self.circle_colors)
        lerp_t = (t * (len(self.circle_colors) - 1)) - color_index

        current_color = lerp_color(
            self.circle_colors[color_index],
            self.circle_colors[next_color_index],
            lerp_t
        )

        # --- Dibujar a Shadow y el círculo ---
        draw_title_shadow(
            self.screen,
            self.screen_width // 2,
            self.screen_height // 2 + 50,
            self.start_time,
            True, # finger_up
            current_color
        )

        # --- Dibujar Texto del Título ---
        draw_text_with_shadow(self.screen, "SHADOW", self.big_title_font, pygame.math.Vector2(self.screen_width // 2, 100), HAIR_BRIGHT_RED, BLACK, reflection=True)
        draw_text_with_shadow(self.screen, "THE HEDGEHOG", self.title_font, pygame.math.Vector2(self.screen_width // 2, 180), WHITE, BLACK, reflection=True)
        draw_text_with_shadow(self.screen, "Press Enter", self.subtitle_font, pygame.math.Vector2(self.screen_width // 2, self.screen_height - 80), GOLD, BLACK)


if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Shadow the Hedgehog - Title Screen")

    title_scene = TitleScreen(screen, screen_width, screen_height)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        next_scene = title_scene.handle_event(event)
        if next_scene:
            print(f"Switching to scene: {next_scene}")
            running = False

        title_scene.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()