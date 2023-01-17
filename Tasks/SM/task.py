import pygame
import random
class Item(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, size, slv, fsv):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size,size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = pygame.math.Vector2(random.randint(slv,fsv), random.randint(slv,fsv))
    
    def update(self):
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        if self.rect.right > WIDTH:
            self.direction.x *= -1
        if self.rect.left < 0:
            self.direction.x *= -1
        if self.rect.bottom > HEIGHT:
            self.direction.y *= -1
        if self.rect.top < 0:
            self.direction.y *= -1
            


def main():
    pygame.init() 
    clock = pygame.time.Clock() 
    
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    surface.fill(WHITE)
    count = 0
    sprites = pygame.sprite.Group()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sprites.empty()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tempRect = pygame.Rect(x, y, 1, 1)
                for sprite in sprites:
                    if tempRect.colliderect(sprite.rect):
                        sprites.remove(sprite)
        if count == 0:
            sprites.add(Item(pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)), 
                            random.randint(60, WIDTH-60), random.randint(60, HEIGHT-60), random.randint(20, 100),
                            SLOWESTVELOCITY, FASTESTVELOCITY))
        
        surface.fill(WHITE)
        sprites.update()
        sprites.draw(surface)
        count += 1
        if count == effectiveSpawnRate:
            count = 0
        pygame.display.update()
        

WIDTH = 800
HEIGHT = 600
FPS = 240 #frames to render per second
framerate = 1/FPS #seconds per frame
SPAWNRATE = 0.01 #spawns per second
effectiveSpawnRate = round(SPAWNRATE * FPS)
FASTESTVELOCITY = 600/FPS #pixels per frame
SLOWESTVELOCITY = 60/FPS #pixels per frame
FASTESTVELOCITY = round(FASTESTVELOCITY)
SLOWESTVELOCITY = round(SLOWESTVELOCITY)
if SLOWESTVELOCITY == 0:
    SLOWESTVELOCITY = 1

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
main()

        