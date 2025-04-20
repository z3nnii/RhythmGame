import pygame
from pygame import mixer

mixer.init()

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

def load(map):
    rects = []
    mixer.music.load(map + ".mp3")
    mixer.music.play()
    f = open(map + ".txt", 'r')
    data = f.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(pygame.Rect(keys[x].rect.x,y * -100,50,25))
    return rects
                

map_rect = load("DeathbyGlamour")

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

    for rect in map_rect:
        pygame.draw.rect(screen,(200,0,0),rect)
        rect.y += 1



    pygame.display.update()
