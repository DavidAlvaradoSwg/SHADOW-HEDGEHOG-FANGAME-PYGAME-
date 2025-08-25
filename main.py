import pygame
import sys
import random
import os
from character import Shadow
from levels import LEVEL_DATA
from background import ProceduralBackground

# --- PANTALLA DE INICIO ---
def show_start_screen(screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SHADOW_RED = (200, 0, 0)
    shadow_frames = []
    shadow_paths = [
        os.path.join('assets', 'characters', 'startgame-shadow1.png'),
        os.path.join('assets', 'characters', 'startgame-shadow2.jpg'),
        os.path.join('assets', 'characters', 'startgame-shadow3.png'),
        os.path.join('assets', 'characters', 'startgame-shadow4.png')
    ]
    try:
        for path in shadow_paths:
            if os.path.exists(path):
                original_image = pygame.image.load(path).convert_alpha()
                original_width, original_height = original_image.get_size()
                aspect_ratio = original_width / original_height
                new_height = 400
                new_width = int(new_height * aspect_ratio)
                scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
                shadow_frames.append(scaled_image)
        if not shadow_frames:
            raise FileNotFoundError("No se cargó ninguna imagen para la animación de inicio.")
        print(f"INFO: {len(shadow_frames)} frames de Shadow cargados para la pantalla de inicio.")
    except (pygame.error, FileNotFoundError) as e:
        print(f"¡ERROR! No se pudo cargar una de las imágenes de Shadow para el inicio: {e}")
        print("INFO: Creando un personaje de reemplazo (rectángulo rojo).")
        fallback_image = pygame.Surface((300, 400)); fallback_image.fill(SHADOW_RED)
        shadow_frames = [fallback_image]

    stars = [{'rect': pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), random.randint(1, 3), random.randint(1, 3)), 'speed': random.randint(1, 3) / 2.0} for _ in range(200)]
    text_font = pygame.font.Font(None, 36)
    credits_font = pygame.font.Font(None, 24)
    overlay_font = pygame.font.Font(None, 90)
    overlay_text_shadow = overlay_font.render("SHADOW THE HEDGEHOG 2D", True, SHADOW_RED)
    overlay_rect_shadow = overlay_text_shadow.get_rect(center=(screen_width / 2 + 4, screen_height * 0.25 + 4))
    overlay_text = overlay_font.render("SHADOW THE HEDGEHOG 2D", True, WHITE)
    overlay_rect = overlay_text.get_rect(center=(screen_width / 2, screen_height * 0.25))
    credits_text = credits_font.render("Fan Game creado por JDSA", True, WHITE)
    credits_rect = credits_text.get_rect(center=(screen_width / 2, screen_height - 30))
    press_start_text = text_font.render("PRESS START", True, WHITE)
    press_start_rect = press_start_text.get_rect(center=(screen_width / 2, screen_height - 80))
    show_text = True
    last_toggle = pygame.time.get_ticks()
    toggle_interval = 600
    current_shadow_frame_index = 0
    last_shadow_toggle = pygame.time.get_ticks()
    shadow_toggle_interval = 250
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                waiting = False
        if pygame.time.get_ticks() - last_shadow_toggle > shadow_toggle_interval:
            current_shadow_frame_index = (current_shadow_frame_index + 1) % len(shadow_frames)
            last_shadow_toggle = pygame.time.get_ticks()
        screen.fill(BLACK)
        for star in stars:
            star['rect'].y += star['speed']
            if star['rect'].y > screen_height:
                star['rect'].y = 0
                star['rect'].x = random.randint(0, screen_width)
            pygame.draw.rect(screen, WHITE, star['rect'])
        shadow_img = shadow_frames[current_shadow_frame_index]
        shadow_rect = shadow_img.get_rect(center=(screen_width / 2, screen_height / 2 + 20))
        screen.blit(shadow_img, shadow_rect)
        screen.blit(overlay_text_shadow, overlay_rect_shadow)
        screen.blit(overlay_text, overlay_rect)
        screen.blit(credits_text, credits_rect)
        if pygame.time.get_ticks() - last_toggle > toggle_interval:
            show_text = not show_text
            last_toggle = pygame.time.get_ticks()
        if show_text:
            screen.blit(press_start_text, press_start_rect)
        pygame.display.flip()
        clock.tick(60)

# --- PANTALLA DE SELECCIÓN DE MAPA ---
def show_map_select_screen(screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SELECTION_COLOR = (255, 255, 0)
    map_ids = list(LEVEL_DATA.keys())
    if not map_ids:
        print("ERROR: No se encontraron mapas en levels.py")
        return None
    THUMB_SIZE = (300, 169)
    loaded_thumbnails = {}
    for map_id in map_ids:
        thumb_path = LEVEL_DATA[map_id].get('thumb')
        thumbnail = None
        if thumb_path and os.path.exists(thumb_path):
            try:
                thumbnail = pygame.image.load(thumb_path).convert_alpha()
                thumbnail = pygame.transform.scale(thumbnail, THUMB_SIZE)
            except pygame.error as e:
                print(f"ADVERTENCIA: No se pudo cargar la miniatura para '{map_id}': {e}. Usando miniatura procedural.")
        if not thumbnail:
            print(f"ADVERTENCIA: No se pudo cargar la miniatura para '{map_id}'. Usando miniatura procedural.")
            map_thumb = pygame.Surface(THUMB_SIZE)
            if "green" in map_id.lower() or "hill" in map_id.lower() or "forest" in map_id.lower():
                map_thumb.fill((150, 200, 255))
                pygame.draw.circle(map_thumb, (50, 150, 50), (THUMB_SIZE[0] // 2, THUMB_SIZE[1] - 30), 80)
                pygame.draw.circle(map_thumb, (60, 160, 60), (THUMB_SIZE[0] // 4, THUMB_SIZE[1] - 50), 70)
                pygame.draw.circle(map_thumb, (40, 140, 40), (THUMB_SIZE[0] * 0.75, THUMB_SIZE[1] - 60), 90)
                pygame.draw.rect(map_thumb, (120, 80, 40), (THUMB_SIZE[0] * 0.6 - 10, THUMB_SIZE[1] - 90, 20, 40))
                pygame.draw.circle(map_thumb, (50, 150, 50), (THUMB_SIZE[0] * 0.6, THUMB_SIZE[1] - 100), 25)
                pygame.draw.circle(map_thumb, (45, 145, 45), (THUMB_SIZE[0] * 0.6 - 15, THUMB_SIZE[1] - 105), 15)
                pygame.draw.circle(map_thumb, (220, 220, 220), (THUMB_SIZE[0] * 0.8, THUMB_SIZE[1] * 0.2), 30)
                pygame.draw.circle(map_thumb, (220, 220, 220), (THUMB_SIZE[0] * 0.7, THUMB_SIZE[1] * 0.25), 25)
            elif "desert" in map_id.lower():
                map_thumb.fill((255, 230, 185))
                pygame.draw.polygon(map_thumb, (210, 170, 130), [(0, THUMB_SIZE[1]), (THUMB_SIZE[0] * 0.3, THUMB_SIZE[1] * 0.8), (THUMB_SIZE[0] * 0.7, THUMB_SIZE[1] * 0.9), (THUMB_SIZE[0], THUMB_SIZE[1])])
                pygame.draw.polygon(map_thumb, (190, 150, 110), [(THUMB_SIZE[0] * 0.4, THUMB_SIZE[1]), (THUMB_SIZE[0] * 0.6, THUMB_SIZE[1] * 0.7), (THUMB_SIZE[0], THUMB_SIZE[1])])
                pygame.draw.polygon(map_thumb, (200, 180, 150), [(50, THUMB_SIZE[1]), (120, THUMB_SIZE[1] // 2), (190, THUMB_SIZE[1])])
                pygame.draw.line(map_thumb, (180, 160, 130), (120, THUMB_SIZE[1] // 2), (120, THUMB_SIZE[1]), 2)
                pygame.draw.circle(map_thumb, (255, 255, 0), (THUMB_SIZE[0] * 0.2, THUMB_SIZE[1] * 0.2), 40)
                pygame.draw.rect(map_thumb, (30, 100, 30), (THUMB_SIZE[0] * 0.8, THUMB_SIZE[1] - 40, 15, 30))
                pygame.draw.rect(map_thumb, (30, 100, 30), (THUMB_SIZE[0] * 0.8 - 15, THUMB_SIZE[1] - 50, 15, 10))
                pygame.draw.rect(map_thumb, (30, 100, 30), (THUMB_SIZE[0] * 0.8 + 15, THUMB_SIZE[1] - 50, 15, 10))
            elif "space" in map_id.lower():
                map_thumb.fill((10, 10, 30))
                for _ in range(3):
                    center_x = random.randint(0, THUMB_SIZE[0])
                    center_y = random.randint(0, THUMB_SIZE[1])
                    for i in range(25):
                        color = (random.randint(50, 150), random.randint(100, 200), random.randint(150, 255), i * 5)
                        pygame.draw.circle(map_thumb, color, (center_x + random.randint(-40, 40), center_y + random.randint(-40, 40)), 2)
                pygame.draw.circle(map_thumb, (200, 50, 50), (THUMB_SIZE[0] * 0.75, THUMB_SIZE[1] * 0.25), 35)
                pygame.draw.circle(map_thumb, (50, 50, 200), (THUMB_SIZE[0] * 0.25, THUMB_SIZE[1] * 0.75), 40)
                pygame.draw.circle(map_thumb, (150, 200, 150), (THUMB_SIZE[0] * 0.5, THUMB_SIZE[1] * 0.5), 20)
                for _ in range(75):
                    pygame.draw.rect(map_thumb, WHITE, (random.randint(0, THUMB_SIZE[0]), random.randint(0, THUMB_SIZE[1]), random.randint(1, 3), random.randint(1, 3)))
            else:
                h = abs(map_id.__hash__())
                map_thumb.fill((h % 50, (h >> 8) % 100, (h >> 16) % 50))
                pygame.draw.polygon(map_thumb, (20, 80, 20), [(0, THUMB_SIZE[1]), (THUMB_SIZE[0]*0.4, THUMB_SIZE[1]*0.5), (THUMB_SIZE[0]*0.6, THUMB_SIZE[1])])
            thumbnail = map_thumb
        loaded_thumbnails[map_id] = thumbnail

    num_maps = len(map_ids)
    padding = 50
    total_width = (num_maps * THUMB_SIZE[0]) + ((num_maps - 1) * padding)
    start_x = (screen_width - total_width) // 2
    map_rects = []
    for i in range(num_maps):
        x = start_x + i * (THUMB_SIZE[0] + padding)
        y = screen_height // 2 - THUMB_SIZE[1] // 2
        map_rects.append(pygame.Rect(x, y, THUMB_SIZE[0], THUMB_SIZE[1]))
    selected_index = 0
    title_font = pygame.font.Font(None, 80)
    map_name_font = pygame.font.Font(None, 40)
    title_text = title_font.render("SELECT A ZONE", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height * 0.2))
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    waiting = False
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(map_ids)
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1 + len(map_ids)) % len(map_ids)
            if event.type == pygame.JOYBUTTONDOWN:
                waiting = False
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        for i, map_id in enumerate(map_ids):
            screen.blit(loaded_thumbnails[map_id], map_rects[i])
        selected_rect = map_rects[selected_index]
        pygame.draw.rect(screen, SELECTION_COLOR, selected_rect.inflate(10, 10), 5)
        selected_map_data = LEVEL_DATA[map_ids[selected_index]]
        map_name_text = map_name_font.render(selected_map_data['name'], True, WHITE)
        map_name_rect = map_name_text.get_rect(center=(screen_width / 2, selected_rect.bottom + 50))
        screen.blit(map_name_text, map_name_rect)
        pygame.display.flip()
        clock.tick(60)
    return map_ids[selected_index]

# --- PANTALLA DE PAUSA ---
def show_pause_screen(screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    WHITE = (255, 255, 255)
    SELECTION_COLOR = (255, 255, 0)
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    title_font = pygame.font.Font(None, 100)
    option_font = pygame.font.Font(None, 60)
    title_text = title_font.render("PAUSA", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height * 0.3))
    options = ["Reanudar", "Volver al Menú Principal"]
    option_rects = []
    selected_index = 0
    for i, option in enumerate(options):
        text = option_font.render(option, True, WHITE)
        rect = text.get_rect(center=(screen_width / 2, screen_height * 0.5 + i * 80))
        option_rects.append(rect)
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1 + len(options)) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if selected_index == 0:
                        return "resume"
                    elif selected_index == 1:
                        return "main_menu"
        screen.blit(overlay, (0, 0))
        screen.blit(title_text, title_rect)
        for i, rect in enumerate(option_rects):
            color = SELECTION_COLOR if i == selected_index else WHITE
            text = option_font.render(options[i], True, color)
            screen.blit(text, rect)
        pygame.display.flip()
        clock.tick(60)

# --- CONFIGURACIÓN PRINCIPAL DEL JUEGO ---
pygame.init()
screen_width = 1400
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shadow Hedgehog Alva Fan Game")
clock = pygame.time.Clock()

# --- ESTADOS DEL JUEGO ---
STATE_START_SCREEN = "start_screen"
STATE_MAP_SELECT = "map_select"
STATE_PLAYING = "playing"
STATE_PAUSE = "pause"
current_state = STATE_START_SCREEN

# --- VARIABLES DEL JUEGO ---
player = None
background = None
selected_level = None
scroll = 0
ground_level = screen_height - 100
player_health = 100

def draw_health_bar(surface, health, max_health):
    bar_width = 200
    bar_height = 20
    fill_width = (health / max_health) * bar_width
    border_rect = pygame.Rect(10, 10, bar_width, bar_height)
    fill_rect = pygame.Rect(10, 10, fill_width, bar_height)
    pygame.draw.rect(surface, (255, 0, 0), border_rect, 2)
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)

# --- BUCLE PRINCIPAL ---
running = True
while running:
    if current_state == STATE_START_SCREEN:
        show_start_screen(screen)
        current_state = STATE_MAP_SELECT
    elif current_state == STATE_MAP_SELECT:
        selected_level = show_map_select_screen(screen)
        if selected_level is None:
            running = False
            continue
        level_data = LEVEL_DATA[selected_level]
        for layer in level_data.get('layers', []):
            if layer.get('type') == 'solid_rect':
                ground_level = layer['rect'][1]
                break
        current_state = STATE_PLAYING
        background = ProceduralBackground(level_data=level_data, screen_width=screen_width, screen_height=screen_height)
        walk_paths = [
            os.path.join('assets', 'characters', 'shadow', 'sprites', 'walk', 'walkshadow1.png'),
            os.path.join('assets', 'characters', 'shadow', 'sprites', 'walk', 'walkshadow2.png'),
            os.path.join('assets', 'characters', 'shadow', 'sprites', 'walk', 'walkshadow3.png')
        ]
        player_start_pos = (100, ground_level)
        player = Shadow(midbottom_pos=player_start_pos, walk_image_paths=walk_paths) 
    elif current_state == STATE_PAUSE:
        action = show_pause_screen(screen)
        if action == "resume":
            current_state = STATE_PLAYING
        elif action == "main_menu":
            current_state = STATE_START_SCREEN
            player = None
            background = None
            selected_level = None
            scroll = 0
    elif current_state == STATE_PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_PAUSE
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_a: # Nueva función de dash con la tecla 'a'
                    player.dash()

        keys = pygame.key.get_pressed()
        
        # El movimiento horizontal ahora solo se procesa si no está haciendo dash
        if not player.is_dashing:
            player_speed = 5
            if keys[pygame.K_LEFT]:
                player.is_walking = True
                player.facing_right = False
                player.rect.x -= player_speed
            elif keys[pygame.K_RIGHT]:
                player.is_walking = True
                player.facing_right = True
                player.rect.x += player_speed
            else:
                player.is_walking = False
        
        # Ahora se le pasa la variable `keys` al método update
        player.update(keys=keys, ground_y=ground_level)
        
        # El scroll se basa en la posición del jugador, manteniendo al jugador centrado
        scroll = player.rect.x - (screen_width // 4)
        
        # Dibujar todo
        if background:
            background.draw(screen, scroll)
        if player:
            player.draw(screen, scroll)
        
        draw_health_bar(screen, player_health, 100) # Asumiendo que esta función está definida
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()