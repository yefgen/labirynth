from pygame import *

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

back = (0, 0, 175)

wind = display.set_mode((700, 500))
display.set_caption('Maze')
wind.fill(back)


class GameSprite(sprite.Sprite):
    def __init__(self, pict, w, h, x, y, s):
        super().__init__()
        self.image = transform.scale(image.load(pict), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def reset(self):
        wind.blit(self.image, (self.rect))


class Wall(sprite.Sprite):
    def __init__(self, w, h, x, y, color=BLACK):
        super().__init__()
        self.color = color
        self.width = w
        self.height = h
        self.image = Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        wind.blit(self.image, self.rect)


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        bullet = Bullet('bullet.png', 10, 10, self.rect.right,self.rect.centery,15)
        bullets.add(bullet)


class Enemy(GameSprite):
    direction = 'top'
    def update(self):
        if self.direction == 'bottom':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        if self.rect.y < 150:
            self.direction = 'bottom'
        if self.rect.y > 429:
            self.direction = 'top'

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()
        


w1 = Wall(250, 15, 200, 300)
w2 = Wall(15, 350, 200, 150)
w3 = Wall(700, 15, 0, 485)
w4 = Wall(700, 15, 0, 0)
w5 = Wall(15, 500, 0, 0)
w6 = Wall(15, 500, 685, 0)

bullets = sprite.Group()

wall_group = sprite.Group()
wall_group.add(w1)
wall_group.add(w2)
wall_group.add(w3)
wall_group.add(w4)
wall_group.add(w5)
wall_group.add(w6)

player = Player('ghost.png', 50, 80, 50, 350, 10)
enemy = Enemy('cyborg.png', 50, 50, 500, 400, 15)
enemy2 = Enemy('cyborg.png', 50, 50, 450, 400, 15)
enemies = sprite.Group()
enemies.add(enemy)
enemies.add(enemy2)
goal = GameSprite('treasure.png', 50, 50, 600, 400, 0)
game = True
finish = False
font.init()
font1 = font.SysFont('Arial', 75)

def create_text(message, color):
    game_over = font1.render(message, True, (255, 255, 255))
    wind.fill(color)
    wind.blit(game_over, (250, 250))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if finish != True:
        wind.fill(back)
        wall_group.draw(wind)
        bullets.update()
        bullets.draw(wind)

        if len(enemies) > 0:
            enemies.draw(wind)
            enemies.update()

        player.reset()
        player.update()
        goal.reset()

    wall_collides = sprite.spritecollide(player, wall_group, False)
    
    if sprite.spritecollide(enemy, bullets, True):
        enemy.rect.x = -100
        enemy.rect.y = -100
        enemy.kill()

    if wall_collides:
        text = 'YOU LOSE!'
        game_over = font1.render(text, True, (255,255,255))
        finish = True
        wind.fill((255,0,0))
        wind.blit(game_over, (250,215))


    if sprite.collide_rect(player, enemy):
        finish = True
        create_text('YOU LOSE!', (255, 0, 0))

    if sprite.collide_rect(player, goal):
        text = 'YOU WIN!'
        game_over = font1.render(text, True, (255,255,255))
        finish = True
        wind.fill((0,255,0))
        wind.blit(game_over, (250, 215))

    sprite.groupcollide(bullets, wall_group, True, False)

    for e in enemies:
        if sprite.spritecollide(e, bullets, True):
            enemies.remove(e)
            e.kill()
        

    
    display.update()
    time.delay(50)