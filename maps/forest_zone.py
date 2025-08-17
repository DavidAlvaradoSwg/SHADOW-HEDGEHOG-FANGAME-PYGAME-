# maps/forest_zone.py
import pygame
import os

class ForestZone:
    """
    Contiene la lógica para el mapa Forest Zone.
    Este archivo de Python se encarga de cargar los datos del nivel
    desde la carpeta 'levels'.
    """
    def __init__(self, screen_width, screen_height, project_root):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.backgrounds = {}
        self.project_root = project_root
        
        # Define los datos para cada acto del mapa
        self.acts = {
            1: {"name": "Forest Zone Act 1", "level_path": os.path.join("levels", "forest_zone_act1.tmx")},
            2: {"name": "Forest Zone Act 2", "level_path": os.path.join("levels", "forest_zone_act2.tmx")},
            3: {"name": "Forest Zone Act 3", "level_path": os.path.join("levels", "forest_zone_act3.tmx")},
        }
        self.current_act_data = None
        self.current_background = None
        self.font = pygame.font.SysFont('Arial', 50, bold=True)
        self._load_backgrounds()

    def _load_backgrounds(self):
        """Carga las imágenes de fondo para cada acto."""
        for act_num in self.acts:
            # Construye la ruta de archivo correcta según tu estructura
            filename = f"forestback{act_num} .jpg" # Nota el espacio
            bg_path = os.path.join(self.project_root, "assets", "backgrounds", "forest-zone", filename)
            
            try:
                background_image = pygame.image.load(bg_path).convert()
                self.backgrounds[act_num] = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
                print(f"Loaded background: {bg_path}")
            except pygame.error:
                # Si no se encuentra la imagen, crea una superficie de color como respaldo
                print(f"Warning: Background '{bg_path}' not found. Using fallback color.")
                fallback_bg = pygame.Surface((self.screen_width, self.screen_height))
                # Colores distintos para cada acto para que se note el cambio
                colors = [(0, 100, 0), (0, 120, 0), (0, 80, 0)]
                fallback_bg.fill(colors[act_num - 1])
                self.backgrounds[act_num] = fallback_bg

    def load_act(self, act_number):
        """Carga los recursos para un acto específico."""
        if act_number in self.acts:
            self.current_act_data = self.acts[act_number]
            self.current_background = self.backgrounds.get(act_number)
            # Aquí es donde en el futuro cargarías el archivo de nivel real usando self.current_act_data['level_path']
            print(f"Cargando {self.current_act_data['name']} desde {self.current_act_data['level_path']}...")
        else:
            print(f"Acto {act_number} no encontrado en Forest Zone.")
            self.current_act_data = None
            self.current_background = None

    def draw(self, screen):
        """Dibuja el estado actual del mapa en la pantalla."""
        if self.current_background:
            screen.blit(self.current_background, (0, 0))
            
            # Dibuja el nombre del acto en la pantalla
            text_surface = self.font.render(self.current_act_data['name'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, 100))
            
            # Sombra para el texto
            shadow_surface = self.font.render(self.current_act_data['name'], True, (0, 0, 0))
            screen.blit(shadow_surface, (text_rect.x + 3, text_rect.y + 3))
            
            screen.blit(text_surface, text_rect)
        else:
            screen.fill((0, 0, 0)) # Pantalla negra si no se carga ningún acto