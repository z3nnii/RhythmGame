import pygame
from pygame import mixer
import time

pygame.init()
mixer.init()

# Screen and font
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Sounds (placeholder: you can add your own .wav files)
# mixer.Sound("perfect.wav"), etc.
hit_sounds = {
    "Perfect": None,
    "Good": None,
    "OK": None,
    "Miss": None
}

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
        self.frames = frames  # List of animation frames (default + dance poses)
        self.default_frame = default_frame  # Default neutral pose
        self.current_frame = default_frame  # Start in the default pose
        self.frame_duration = 10  # Duration each frame lasts
        self.frame_timer = 0  # Timer to keep track of frame changes
        self.is_dancing = False  # Flag to check if the character is in a dance pose

    def update(self):
        # Update the frame based on the timer (smooth transitions between frames)
        if self.is_dancing:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                # Stop dancing after the last frame of the dance pose
                if self.current_frame == 0:
                    self.is_dancing = False  # Reset to default pose after dance ends

    def draw(self, surface):
        # Draw the current animation frame at the character's position
        surface.blit(self.frames[self.current_frame], (self.x, self.y))

    def trigger_dance(self, dance_pose):
        self.current_frame = dance_pose  # Start a new dance pose
        self.is_dancing = True  # Start the dancing animation
        self.frame_timer = 0  # Reset the frame timer

    def reset_to_default(self):
        self.current_frame = self.default_frame  # Reset animation to the default pose
        self.frame_timer = 0
        self.is_dancing = False

# Keys and Keybinds
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

# Load character animation frames (replace these with your own images)
# Assuming you have 4 frames for the animation, one for each dance pose
# Load all frames: default (standing) pose + 4 dance poses
character_frames = [
    pygame.image.load("default_pose.png").convert_alpha(),  # Default pose
    pygame.image.load("dance_pose_1.png").convert_alpha(),
    pygame.image.load("dance_pose_2.png").convert_alpha(),
    pygame.image.load("dance_pose_3.png").convert_alpha(),
    pygame.image.load("dance_pose_4.png").convert_alpha(),
]

# Default pose is the first frame (standing pose)
default_frame = 0

# Create the character instance
character = Character(350, 300, character_frames, default_frame)

# Key states for A, S, D, F, triggering the dance poses
key_dances = {
    pygame.K_a: 1,  # First dance pose for A
    pygame.K_s: 2,  # Second dance pose for S
    pygame.K_k: 3,  # Third dance pose for k
    pygame.K_l: 4   # Fourth dance pose for l
}
# Load song and map
def load(map):
    rects = []
    mixer.music.load(map + ".mp3")
    mixer.music.play()
    with open(map + ".txt", 'r') as f:
        data = [line.strip() for line in f.readlines()]
    for y in range(len(data)):
        for x in range(min(len(data[y]), len(keys))):
            if data[y][x] == '0':
                rects.append(pygame.Rect(keys[x].rect.centerx - 25, y * -100, 50, 25))
    return rects

# Game state
hit_effects = []  # (text, x, y, life)
score = 0
combo = 0

map_rect = load("DeathbyGlamour")

#Main game loop

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

     # Handle key presses for dancing
    k = pygame.key.get_pressed()

    # Check if any key in A, S, D, F is pressed
    dancing = False
    for key in key_dances:
        if k[key]:  # If a key is pressed (A, S, D, F)
            character.trigger_dance(key_dances[key])  # Trigger the corresponding dance pose
            dancing = True

    # If no keys are pressed, reset to the default pose
    if not dancing:
        character.reset_to_default()

    # Update the character's animation
    character.update()

    # Draw the character (default pose or dance pose)
    character.draw(screen)

    # Draw hit line
    pygame.draw.line(screen, (255, 255, 255), (0, keys[0].rect.centery), (800, keys[0].rect.centery), 2)

    # Key press detection
    k = pygame.key.get_pressed()
    for key in keys:
        if k[key.key]:
            pygame.draw.rect(screen, key.color1, key.rect)
            key.handled = False
        else:
            pygame.draw.rect(screen, key.color2, key.rect)
            key.handled = True

    # Falling note logic
    for rect in map_rect[:]:
        pygame.draw.rect(screen, (200, 0, 0), rect)
        rect.y += 5

        for key in keys:
            distance = abs(rect.centery - key.rect.centery)
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
                    if hit_sounds[rating]:
                        hit_sounds[rating].play()
                    hit_effects.append((rating, key.rect.centerx, key.rect.top - 40, 60))
                    map_rect.remove(rect)
                    key.handled = True
                    break

    # Missed notes
    for rect in map_rect[:]:
        if rect.top > 600:
            map_rect.remove(rect)
            rating = "Miss"
            score -= 25
            combo = 0
            if hit_sounds[rating]:
                hit_sounds[rating].play()
            hit_effects.append((rating, rect.centerx, keys[0].rect.top - 40, 60))

    # Draw feedback
    for effect in hit_effects[:]:
        text, x, y, life = effect
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (x - label.get_width() // 2, y))
        life -= 1
        if life <= 0:
            hit_effects.remove(effect)
        else:
            hit_effects[hit_effects.index(effect)] = (text, x, y, life)

    # Score + combo display
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    combo_text = font.render(f"Combo: {combo}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    screen.blit(combo_text, (20, 60))

    pygame.display.update()
    clock.tick(60)
