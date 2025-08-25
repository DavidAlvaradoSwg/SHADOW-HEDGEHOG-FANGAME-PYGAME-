import pygame
import random
import math

class ProceduralBackground:
    def __init__(self, level_data, screen_width, screen_height):
        self.layers = level_data.get('layers', [])
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_name = level_data.get('name', 'unknown')

        self.pattern_widths = {}
        for i, layer in enumerate(self.layers):
            layer_type = layer.get('type')
            if layer_type in ['rects', 'circles', 'polygons']:
                max_x = 0
                elements = layer.get('elements', [])
                if not elements:
                    self.pattern_widths[i] = self.screen_width
                    continue
                for element in elements:
                    if layer_type == 'rects':
                        if element[0] + element[2] > max_x:
                            max_x = element[0] + element[2]
                    elif layer_type == 'circles':
                        if element[0] + element[2] > max_x:
                            max_x = element[0] + element[2]
                    elif layer_type == 'polygons':
                        for point in element:
                            if point[0] > max_x:
                                max_x = point[0]
                self.pattern_widths[i] = max_x if max_x > 0 else self.screen_width

        # Detalles específicos de cada zona
        if self.level_name.lower() == 'cityspace_zone':
            self.stars = [
                {'rect': pygame.Rect(random.randint(0, self.screen_width), random.randint(0, self.screen_height), random.randint(1, 3), random.randint(1, 3)), 'speed': random.uniform(0.1, 0.5)} for _ in range(200)
            ]
            self.asteroids = [
                {'pos': [random.uniform(0, self.screen_width), random.uniform(0, self.screen_height)], 'radius': random.randint(5, 20), 'speed': random.uniform(0.05, 0.15), 'color': (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150))} for _ in range(10)
            ]
        elif self.level_name.lower() == 'desert_zone':
            self.dust_particles = [
                {'pos': [random.uniform(0, self.screen_width), random.uniform(0, self.screen_height)], 'radius': random.randint(1, 3), 'speed': random.uniform(0.2, 0.6)} for _ in range(50)
            ]
        elif self.level_name.lower() == 'forest_zone':
            self.fog_particles = [
                {'pos': [random.uniform(0, self.screen_width), random.uniform(0, self.screen_height)], 'radius': random.randint(5, 15), 'speed': random.uniform(0.1, 0.3)} for _ in range(30)
            ]

    def draw(self, surface, scroll_x):
        for i, layer in enumerate(self.layers):
            layer_type = layer.get('type')
            color = layer.get('color', (0, 0, 0))
            speed = layer.get('speed', 1.0)
            layer_scroll = scroll_x * speed

            if layer_type == 'solid_color':
                surface.fill(color)
                # Capa de atmósfera (niebla/polvo)
                if self.level_name.lower() == 'desert_zone':
                    self._draw_dynamic_particles(surface, self.dust_particles, layer_scroll * 0.5, (220, 190, 130, 50))
                elif self.level_name.lower() == 'forest_zone':
                    self._draw_dynamic_particles(surface, self.fog_particles, layer_scroll * 0.3, (200, 220, 200, 75))

            elif layer_type == 'solid_rect':
                rect_data = layer.get('rect')
                if not rect_data or len(rect_data) < 4:
                    continue
                pygame.draw.rect(surface, color, (0, rect_data[1], self.screen_width, self.screen_height - rect_data[1]))

            elif layer_type == 'rects':
                pattern_width = self.pattern_widths.get(i, self.screen_width)
                scroll_offset = layer_scroll % pattern_width
                elements = layer.get('elements', [])
                for element_data in elements:
                    x_base, y, w, h = element_data
                    x_pos = x_base - scroll_offset
                    self._draw_detailed_rect(surface, color, (x_pos, y, w, h), self.level_name)
                    self._draw_detailed_rect(surface, color, (x_pos + pattern_width, y, w, h), self.level_name)

            elif layer_type == 'circles':
                pattern_width = self.pattern_widths.get(i, self.screen_width)
                scroll_offset = layer_scroll % pattern_width
                elements = layer.get('elements', [])
                for element_data in elements:
                    cx_base, cy, r = element_data
                    cx_pos = cx_base - scroll_offset
                    self._draw_detailed_circle(surface, color, (cx_pos, cy, r), self.level_name)
                    self._draw_detailed_circle(surface, color, (cx_pos + pattern_width, cy, r), self.level_name)

            elif layer_type == 'polygons':
                pattern_width = self.pattern_widths.get(i, self.screen_width)
                scroll_offset = layer_scroll % pattern_width
                elements = layer.get('elements', [])
                for poly_points in elements:
                    points = [(p[0] - scroll_offset, p[1]) for p in poly_points]
                    pygame.draw.polygon(surface, color, points)
                    points_copy = [(p[0] + pattern_width - scroll_offset, p[1]) for p in poly_points]
                    pygame.draw.polygon(surface, color, points_copy)
        
        # Dibujar elementos dinámicos después de las capas estáticas
        if self.level_name.lower() == 'cityspace_zone':
            for star in self.stars:
                star['rect'].x = (star['rect'].x - scroll_x * star['speed']) % self.screen_width
                if star['rect'].x < 0:
                    star['rect'].x += self.screen_width
                pygame.draw.rect(surface, (255, 255, 255), star['rect'])
            for asteroid in self.asteroids:
                asteroid['pos'][0] -= asteroid['speed']
                if asteroid['pos'][0] < -asteroid['radius']:
                    asteroid['pos'][0] = self.screen_width + asteroid['radius']
                pygame.draw.circle(surface, asteroid['color'], (int(asteroid['pos'][0]), int(asteroid['pos'][1])), asteroid['radius'])

    def _draw_detailed_rect(self, surface, color, rect_data, level_name):
        x, y, w, h = rect_data
        
        # Efecto 3D simple
        darker_color = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
        lighter_color = (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20))
        pygame.draw.rect(surface, darker_color, (x, y, w, h))
        pygame.draw.rect(surface, color, (x + 2, y + 2, w - 4, h - 4))
        pygame.draw.rect(surface, lighter_color, (x + 2, y + 2, w - 4, 2))
        
        # Detalles específicos de nivel
        if level_name.lower() == 'forest_zone':
            tree_top_color = (50, 150, 50)
            pygame.draw.circle(surface, tree_top_color, (int(x + w * 0.5), int(y + h * 0.2)), int(w * 0.5))
        elif level_name.lower() == 'desert_zone':
            cactus_color = (34, 139, 34)
            pygame.draw.rect(surface, cactus_color, (x + w*0.45, y + h*0.2, w*0.1, h*0.8))
        elif level_name.lower() == 'cityspace_zone':
            window_color = (255, 255, 150)
            for row in range(5):
                for col in range(5):
                    win_x, win_y = x + col * 10 + 5, y + row * 10 + 5
                    pygame.draw.rect(surface, window_color, (win_x, win_y, 5, 5))

    def _draw_detailed_circle(self, surface, color, circle_data, level_name):
        cx, cy, r = circle_data
        if level_name.lower() == 'forest_zone':
            pygame.draw.circle(surface, (color[0], color[1], color[2], 100), (int(cx), int(cy)), int(r), 0)
        elif level_name.lower() == 'cityspace_zone':
            pygame.draw.circle(surface, color, (int(cx), int(cy)), int(r))
            crater_color = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
            pygame.draw.circle(surface, crater_color, (int(cx - r * 0.4), int(cy - r * 0.1)), int(r * 0.2))

    def _draw_dynamic_particles(self, surface, particles, scroll_offset, color):
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for particle in particles:
            particle['pos'][0] = (particle['pos'][0] - particle['speed'] * 0.5 - scroll_offset) % self.screen_width
            pygame.draw.circle(s, color, (int(particle['pos'][0]), int(particle['pos'][1])), particle['radius'])
        surface.blit(s, (0, 0))