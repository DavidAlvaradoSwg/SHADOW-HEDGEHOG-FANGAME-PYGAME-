import pygame
import os

class Shadow:
    def __init__(self, midbottom_pos, walk_image_paths):
        self.walk_frames = []
        self.jump_frame = None
        standard_height = 128
        
        # Cargar frames de caminata
        try:
            for path in walk_image_paths:
                image = pygame.image.load(path).convert_alpha()
                width, height = image.get_size()
                aspect = width / height
                scaled_image = pygame.transform.scale(image, (int(standard_height * aspect), standard_height))
                self.walk_frames.append(scaled_image)
            
            # Cargar el nuevo frame de salto (la bola)
            jump_path = os.path.join('assets', 'characters', 'shadow', 'sprites', 'sphere', 'sphere4.png')
            self.jump_frame = pygame.transform.scale(pygame.image.load(jump_path).convert_alpha(), (int(standard_height * 0.8), standard_height))
        except (pygame.error, FileNotFoundError) as e:
            print(f"ERROR: No se pudieron cargar los sprites de Shadow. {e}")
            fallback_image = pygame.Surface((40, 60)); fallback_image.fill((255, 0, 0))
            self.walk_frames.append(fallback_image)
            self.jump_frame = fallback_image

        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(midbottom=midbottom_pos)
        
        self.is_walking = False
        self.is_jumping = False
        self.is_dashing = False
        self.facing_right = True

        self.animation_speed = 0.2
        self.current_frame_index = 0

        self.jump_strength = -20  # Aumentado para un salto más alto
        self.gravity = 0.8
        self.y_velocity = 0
        self.on_ground = True
        
        self.dash_speed = 15

    def jump(self):
        if self.on_ground and not self.is_dashing:
            self.y_velocity = self.jump_strength
            self.on_ground = False
            self.is_jumping = True

    def dash(self):
        """Activa el estado de dash si está en el suelo."""
        if self.on_ground and not self.is_dashing:
            self.is_dashing = True
            self.is_walking = False

    def update(self, keys, ground_y):
        # --- Lógica de Dash y Frenado ---
        if self.is_dashing:
            # Frena si se presiona la tecla de dirección opuesta
            if (self.facing_right and keys[pygame.K_LEFT]) or \
               (not self.facing_right and keys[pygame.K_RIGHT]):
                self.is_dashing = False
            else:
                # Aplica el movimiento del dash
                move_direction = 1 if self.facing_right else -1
                self.rect.x += self.dash_speed * move_direction

        # --- Física (Gravedad) ---
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # --- Colisión con el suelo ---
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.y_velocity = 0
            if not self.on_ground: # Si acaba de aterrizar
                self.is_dashing = False # Detiene el dash al tocar el suelo
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False

        # --- Actualización de la animación ---
        if self.is_dashing or self.is_jumping:
            self.image = self.jump_frame
        elif self.is_walking:
            self.current_frame_index += self.animation_speed
            if self.current_frame_index >= len(self.walk_frames):
                self.current_frame_index = 0
            self.image = self.walk_frames[int(self.current_frame_index)]
        else:
            self.image = self.walk_frames[0]

        # --- Voltear el sprite si es necesario ---
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface, scroll):
        draw_x = self.rect.x - scroll
        surface.blit(self.image, (draw_x, self.rect.y))