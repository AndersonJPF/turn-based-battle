import pygame, sys
import random


### Settings ###
width = 900
height = 900
FPS = 30

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTBLUE = (0, 155, 155)

pygame.init()

### Primary Definitions ###
background = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("Turn-based battle")
font_name = pygame.font.match_font('Monospace')

### Functions and Sprites ###

def health_bar(x, y, w, hp, max_hp):
    if hp < 0:
        hp = 0
    fill = (hp/max_hp) * w
    outline_rect = pygame.Rect(x, y, w, 10)
    filled_rect = pygame.Rect(x+1, y+1, fill-2, 8)
    pygame.draw.rect(background, WHITE, outline_rect, 1)
    pygame.draw.rect(background, GREEN, filled_rect)

def turn(character):
    character.turn = True
    if character in enemies:
        target = random.choice(party)
        character.attack(target)

# Sprites ###
class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.image = pygame.Surface((100, 40))
        self.rect = self.image.get_rect()
        self.image.fill(GRAY)
        self.rect.centerx = width / 2
        self.rect.centery = 3 * height / 4
        self.text = 'Attack'
        self.font = pygame.font.Font(font_name, 16)
        self.image.blit(self.font.render(self.text, True, WHITE), (20, 10))
        self.able = False
    
    def update(self):
        self.image.fill(GRAY)
        self.image.blit(self.font.render(self.text, True, WHITE), (20, 10))
        #pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, COL, speed):
        pygame.sprite.Sprite.__init__(self, all_sprites, characters, heroes)
        self.image = pygame.Surface([30, 30])
        self.image.fill(COL)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.max_hp = 100
        self.hp = 100
        self.strength = 10
        self.speed = speed
        self.turn = False
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp, self.max_hp)

    def attack(self, target):
        if self.turn:
            Value('Attack', self, WHITE)
            hit = int(random.randrange(0.8 * self.strength, 1.2 * self.strength))
            rng = random.randint(1, 101)
            if rng <= 20:
                hit *= 2
                target.hp -= hit
                #attack_announce(self)
                Value(hit, target, WHITE)
            else:
                target.hp -= hit
                #attack_announce(self)
                Value(hit, target, RED)
            self.turn = False
            sortedbyspeed.remove(self)
            sortedbyspeed.append(self)

    def update(self):
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp, self.max_hp)
        if self.hp <= 0:
            self.kill()

class Red_box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, all_sprites, characters, enemies)
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.max_hp = 300
        self.hp = self.max_hp
        self.strength = 20
        self.speed = 25
        self.turn = False
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp, self.max_hp)

    def attack(self, target):
        if self.turn:
            Value('Attack', self, WHITE)
            hit = int(random.randrange(0.8 * self.strength, 1.2 * self.strength))
            rng = random.randint(1, 101)
            if rng <= 20:
                hit *= 2
                target.hp -= hit
                Value(hit, target, WHITE)
            else:
                target.hp -= hit
                Value(hit, target, RED)
            self.turn = False
            sortedbyspeed.remove(self)
            sortedbyspeed.append(self)
    
    def update(self):
        health_bar(self.rect.x, self.rect.top - 12, self.rect.width, self.hp, self.max_hp)
        if self.hp <= 0:
            self.kill()

    
class Value(pygame.sprite.Sprite):
    def __init__(self, value, target, color):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.font = pygame.font.Font(font_name, 24)
        self.image = self.font.render(str(value), True, color)
        self.rect = self.image.get_rect()
        self.owner = target
        self.rect.bottomright = target.rect.topleft
    
    def update(self):
        self.rect.y -= 1
        if self.owner.rect.y - self.rect.y >= 75:
            self.kill()

### Creating Sprites ###
all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
heroes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player(width / 4, height / 2, YELLOW, 15)
player2 = Player(width/4 - 50, height/2, LIGHTBLUE, 15)
enemy = Red_box(3 * width / 4, height / 2)
button = Button()

### Time-related stuff ###
cooldown = 1000
last_turn = 0

### Background music ###
#pygame.mixer.music.load('battle.wav')
#pygame.mixer.music.play(-1)

### Main Loop ###
sortedbyspeed = sorted(characters, key=lambda x: x.speed, reverse=True)
party = []
mobs = []

for char in sortedbyspeed:
    if char in heroes:
        party.append(char)
    if char in enemies:
        mobs.append(char)

while len(heroes) > 0 and len(enemies) > 0:
    clock.tick(60)
    countdown = pygame.time.get_ticks()
    if countdown - last_turn > cooldown:
        turn(sortedbyspeed[0])
        last_turn = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(event.pos):
                if sortedbyspeed[0] in heroes:
                    sortedbyspeed[0].attack(enemy)

    for char in sortedbyspeed:
        if char.hp <= 0:
            sortedbyspeed.remove(char)
            if char in party:
                party.remove(char)
            if char in mobs:
                mobs.remove(char)
                
    #print(len(sortedbyspeed))
    background.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(background)
    pygame.display.update()

pygame.quit()
sys.exit()