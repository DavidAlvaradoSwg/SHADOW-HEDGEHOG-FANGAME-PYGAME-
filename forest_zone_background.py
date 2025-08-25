import pygame

class ProceduralBackground:
    def __init__(self, level_data, screen_width, screen_height):
        self.layers = level_data.get('layers', [])
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Para los elementos que se repiten, calculamos el ancho total del patrón.
        self.pattern_widths = {}
        for i, layer in enumerate(self.layers):
            if layer.get('type') == 'rects':
                max_x = 0
                for element in layer.get('elements', []):
                    # element es [x, y, w, h]
                    if element[0] + element[2] > max_x:
                        max_x = element[0] + element[2]
                # Usamos el ancho de la pantalla como un extra para asegurar el bucle
                self.pattern_widths[i] = max_x if max_x > 0 else self.screen_width

    def draw(self, surface, scroll_x):
        """
        Dibuja todas las capas del fondo en la superficie dada.
        - surface: La pantalla de Pygame donde se va a dibujar.
        - scroll_x: El desplazamiento horizontal total del mundo.
        """
        # Dibujamos las capas desde el fondo hacia el frente
        for i, layer in enumerate(self.layers):
            layer_type = layer.get('type')

            if layer_type == 'solid_color':
                
                surface.fill(layer['color'])

            elif layer_type == 'solid_rect':
                color = layer['color']
                rect_data = layer['rect']
                # Asumimos que este rectángulo es el suelo y ocupa todo el ancho
                pygame.draw.rect(surface, color, (0, rect_data[1], self.screen_width, rect_data[3]))

            elif layer_type == 'rects':
                speed = layer.get('speed', 0.5)
                color = layer['color']
                layer_scroll = scroll_x * speed
                pattern_width = self.pattern_widths.get(i, self.screen_width)

                for element in layer.get('elements', []):
                    base_x, y, w, h = element
                    
                    # Para que el patrón se repita, usamos el módulo del ancho del patrón
                    scroll_offset = layer_scroll % pattern_width
                    x_pos = base_x - scroll_offset
                    
                    # Dibujamos el elemento y sus copias para el bucle infinito
                    pygame.draw.rect(surface, color, (x_pos, y, w, h))
                    pygame.draw.rect(surface, color, (x_pos + pattern_width, y, w, h))
                    pygame.draw.rect(surface, color, (x_pos - pattern_width, y, w, h))
