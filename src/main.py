import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def load_key_images(normal_path, pressed_path):
    normal = pygame.image.load(normal_path).convert_alpha()
    pressed = pygame.image.load(pressed_path).convert_alpha()
    normal = pygame.transform.scale(normal, (80, 80))
    pressed = pygame.transform.scale(pressed, (80, 80))
    return normal, pressed

class Key():
    def __init__(self, x, y, image_normal, image_pressed, key_code):
        self.image_normal = image_normal
        self.image_pressed = image_pressed
        self.image = image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.key_code = key_code
        self.pressed = False

    def update(self):
        self.pressed = pygame.key.get_pressed()[self.key_code]
        self.image = self.image_pressed if self.pressed else self.image_normal

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Load all images
a_normal, a_pressed = load_key_images("assets/key_a.png", "assets/key_a_pressed.png")
s_normal, s_pressed = load_key_images("assets/key_s.png", "assets/key_s_pressed.png")
j_normal, j_pressed = load_key_images("assets/key_j.png", "assets/key_j_pressed.png")
k_normal, k_pressed = load_key_images("assets/key_k.png", "assets/key_k_pressed.png")

# Create keys
keys = [
    Key(100, 100, a_normal, a_pressed, pygame.K_a),
    Key(200, 100, s_normal, s_pressed, pygame.K_s),
    Key(500, 100, j_normal, j_pressed, pygame.K_j),
    Key(600, 100, k_normal, k_pressed, pygame.K_k),
]

# Game loop
while True:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for key in keys:
        key.update()
        key.draw(screen)

    pygame.display.update()
    clock.tick(60)