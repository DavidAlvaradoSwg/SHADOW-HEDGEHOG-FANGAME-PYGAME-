# character.py
import pygame

class Shadow:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surf):
        surf.blit(self.image, self.rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Cargar la imagen de Shadow (usa la ruta de tu archivo PNG con transparencia)
    shadow = Shadow(400, 300, "shadow-removebg.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((100, 150, 255))
        shadow.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
