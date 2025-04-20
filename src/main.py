import pygame

screen = pygame.display.set_mode((800, 600))

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
    Key(100,100,(255,0,0),(0,0,0),pygame.K_f),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
