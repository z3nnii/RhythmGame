import pygame
from pygame import mixer

mixer.init()
mixer.music.load('')

screen = pygame.display.set_mode((800, 600))

class Key():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,50,20)

keys = [
    Key(100,500,(255,0,0),(220,0,0),pygame.K_a),
    Key(200,500,(0,255,0),(0,220,0),pygame.K_s),
    Key(300,500,(0,0,255),(0,0,220),pygame.K_d),
    Key(400,500,(255,255,0),(220,220,0),pygame.K_f),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    k = pygame.key.get_pressed()
    for key in keys:
        if k[key.key]:
            pygame.draw.rect(screen,key.color1,key.rect)
        if not k[key.key]:
            pygame.draw.rect(screen,key.color2,key.rect)



    pygame.display.update()
