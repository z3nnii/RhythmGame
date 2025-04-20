import pygame

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
    Key(100,100,(255,0,0),(220,0,0),pygame.K_a),
    Key(200,100,(0,255,0),(0,220,0),pygame.K_s),
    Key(300,100,(0,0,255),(0,0,220),pygame.K_d),
    Key(400,100,(255,255,0),(220,220,0),pygame.K_f),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for key in keys:
        pygame.draw.rect(screen,key.color1,key.rect)



    pygame.display.update()
