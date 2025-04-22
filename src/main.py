import pygame
from pygame import mixer
import time

pygame.init()

# Screen and font
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Key class
class Key():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 100, 40)
        self.handled = False

class Character():
    def __init__(self, x, y, frames, default_frame):
        self.x = x
        self.y = y
        self.frames = frames
        self.default_frame = default_frame
        self.current_frame = default_frame
        self.frame_duration = 10
        self.frame_timer = 0
        self.is_dancing = False

    def update(self):
        if self.is_dancing:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                if self.current_frame == 0:
                    self.is_dancing = False

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], (self.x, self.y))

    def trigger_dance(self, dance_pose):
        self.current_frame = dance_pose
        self.is_dancing = True
        self.frame_timer = 0

    def reset_to_default(self):
        self.current_frame = self.default_frame
        self.frame_timer = 0
        self.is_dancing = False

key_width = 100
spacing = 20
start_x = (800 - (4 * key_width + 3 * spacing)) // 2
keys = [
    Key(start_x + i * (key_width + spacing), 500, color1, color2, key)
    for i, (color1, color2, key) in enumerate([
        ((255, 0, 0), (220, 0, 0), pygame.K_a),
        ((0, 255, 0), (0, 220, 0), pygame.K_s),
        ((0, 0, 255), (0, 0, 220), pygame.K_k),
        ((255, 255, 0), (220, 220, 0), pygame.K_l)
    ])
]

character_frames = [
    pygame.image.load("default_pose.png").convert_alpha(),
    pygame.image.load("dance_pose_1.png").convert_alpha(),
    pygame.image.load("dance_pose_2.png").convert_alpha(),
    pygame.image.load("dance_pose_3.png").convert_alpha(),
    pygame.image.load("dance_pose_4.png").convert_alpha(),
]

character = Character(350, 300, character_frames, 0)

key_dances = {
    pygame.K_a: 1,
    pygame.K_s: 2,
    pygame.K_k: 3,
    pygame.K_l: 4
}

class Note:
    def __init__(self, rect, lane_index):
        self.rect = rect
        self.lane_index = lane_index
        self.color = (200, 0, 0)

map_notes = []

def load(map):
    mixer.music.load(map + ".mp3")
    mixer.music.play()
    with open(map + ".txt", 'r') as f:
        data = [line.strip() for line in f.readlines()]
    for y in range(len(data)):
        for x in range(min(len(data[y]), len(keys))):
            if data[y][x] == '0':
                rect = pygame.Rect(keys[x].rect.centerx - 25, y * -100, 50, 25)
                map_notes.append(Note(rect, x))

load("DeathbyGlamour")

hit_effects = []
score = 0
combo = 0

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    k = pygame.key.get_pressed()
    dancing = False
    for key in key_dances:
        if k[key]:
            character.trigger_dance(key_dances[key])
            dancing = True
    if not dancing:
        character.reset_to_default()

    character.update()
    character.draw(screen)

    pygame.draw.line(screen, (255, 255, 255), (0, keys[0].rect.centery), (800, keys[0].rect.centery), 2)

    for key in keys:
        if k[key.key]:
            pygame.draw.rect(screen, key.color1, key.rect)
            key.handled = False
        else:
            pygame.draw.rect(screen, key.color2, key.rect)
            key.handled = True

    for note in map_notes[:]:
        note.rect.y += 5
        key = keys[note.lane_index]

        pygame.draw.rect(screen, note.color, note.rect)
        distance = abs(note.rect.centery - key.rect.centery)
        if distance < 40 and not key.handled:
            if k[key.key]:
                if distance < 10:
                    rating = "Perfect"
                    score += 100
                    combo += 1
                elif distance < 25:
                    rating = "Good"
                    score += 70
                    combo += 1
                else:
                    rating = "OK"
                    score += 40
                    combo += 1
                hit_effects.append((rating, key.rect.centerx, key.rect.top - 40, 60))
                map_notes.remove(note)
                key.handled = True

    for note in map_notes[:]:
        if note.rect.top > 600:
            map_notes.remove(note)
            rating = "Miss"
            score -= 25
            combo = 0
            hit_effects.append((rating, note.rect.centerx, keys[0].rect.top - 40, 60))

    for effect in hit_effects[:]:
        text, x, y, life = effect
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (x - label.get_width() // 2, y))
        life -= 1
        if life <= 0:
            hit_effects.remove(effect)
        else:
            hit_effects[hit_effects.index(effect)] = (text, x, y, life)

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 20))
    screen.blit(font.render(f"Combo: {combo}", True, (255, 255, 255)), (20, 60))

    pygame.display.update()
    clock.tick(60)




