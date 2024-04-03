from pygame import *
from random import randint
font.init()

lost = 0
pobeda = 0

win = display.set_mode((700,500))
display.set_caption('Shooter of Galaxy')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
clock = time.Clock()
FPS = 60
finish = False
font2 = font.SysFont('Arial', 36)

class godgod(sprite.Sprite):
    def __init__(self, image1, x, y, speed, weith, height):
        super().__init__()
        self.image = transform.scale(image.load(image1),(weith, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(godgod):
    def Move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 590:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(godgod):
    def update(self):
        self.rect.y += self.speed
        global lost
        global pobeda
        if self.rect.y >= 500:
            self.rect.x = randint(80, 420 - 80)
            self.rect.y = 0
            lost = lost + 1
            self.rect.x = randint(50,650)

class Bullet(godgod):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
player = Rocket(('rocket.png'), 300, 400, 8, 100, 100)
debil = Enemy(('ufo.png'), 100, 100, 3, 80, 80)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(('ufo.png'), randint (80, 420 - 80), 100, randint(1, 4), 80, 80)
    monsters.add(monster)



game = True
while game:
    if finish != True:
        win.blit(background, (0,0))
        player.reset()
        player.Move()
        lose = font2.render('ПОЗОРИЩЕ!', True, (255, 0, 0))
        win2 = font2.render('ПОБЕДА!', True, (255, 130, 0))
        monsters.update()
        monsters.draw(win)
        bullets.update()
        bullets.draw(win)
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_win = font2.render("Счёт: " + str(pobeda), 1, (235, 100, 0))
        win.blit(text_lose, (10, 60))
        win.blit(text_win, (10, 30))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        if sprite_list:
            pobeda += 1
            monster = Enemy(('ufo.png'), randint (80, 420 - 80), 100, randint(1, 4), 80, 80)
            monsters.add(monster)

        if pobeda == 10:
            win.blit(win2, (200, 200))
            finish = True
        sprite_list2 = sprite.spritecollide(player, monsters, False)
        if lost == 3:
            win.blit(lose, (200, 200))
            finish = True
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()        
    clock.tick(FPS)
    display.update()