import pygame

screen = pygame.display.set_mode((800, 600))

def load_key_images(normal_path, pressed_path):
    normal = pygame.image.load(normal_path).convert_alpha()
    pressed = pygame.image.load(pressed_path).convert_alpha()
    normal = pygame.transform.scale(normal, (80, 80))
    pressed = pygame.transform.scale(pressed, (80, 80))
    return normal, pressed

class Key():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key

key = [
    Key(100,100,(255,0,0),(0,0,0),pygame.K_a),
    Key(100,100,(255,0,0),(0,0,0),pygame.K_s),
    Key(100,100,(255,0,0),(0,0,0),pygame.K_d),
    Key(100,100,(255,0,0),(0,0,0),pygame.K_f)
]




# Load all images
a_normal, a_pressed = load_key_images("assets/key_a.png", "assets/key_a_pressed.png")
s_normal, s_pressed = load_key_images("assets/key_s.png", "assets/key_s_pressed.png")
j_normal, j_pressed = load_key_images("assets/key_j.png", "assets/key_j_pressed.png")
k_normal, k_pressed = load_key_images("assets/key_k.png", "assets/key_k_pressed.png")

