from random import randint
from pygame import *
import time as Time
window = display.set_mode((1000, 700))
display.set_caption('Название игры')
fon = transform.scale(image.load('galaxy.jpg'), (1000,700))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')

finish = False
font.init()
font = font.Font(None, 35)
score = 0
miss = 0
finish = False
ammo = 30
r = False

class Gamer(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y, size_x, size_y, player_speed, start_t):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.start_t = start_t
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def stop(self):
        self.speed = 0
    def death(self):
        self.player_x = 1001
        self.player_y = 1001
        self.size_x = 0
        self.size_y = 0
class Hero(Gamer):
    def Control(self):
        control = key.get_pressed()
        if control[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed 
        if control[K_d] and self.rect.x < 920:
            self.rect.x += self.speed
    def fire(self):
        controls = key.get_pressed()
        global finish
        global ammo
        global r
        if controls[K_SPACE] and r==False and finish == False:
            bullet = Bullet('bullet.png', self.rect.x+40, self.rect.y, 15, 20, 7, 0)
            bullets.add(bullet)
            bullet.arrive()
            shot.play()
            ammo -= 1
        if ammo==0 and r == False:
            self.start_t = int(Time.time())
            r = True

                
            
            
class Bullet(Gamer):
    def arrive(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy_1(Gamer):
    def control_1(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > 700:

            self.rect.y = 0
            self.rect.x = randint(0, 920)
class Enemy(Gamer):
    def control_1(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > 700:
            miss += 1
            self.rect.y = 0
            self.rect.x = randint(0, 920)
    def death(self):
        global score
        if sprite.groupcollide(enemies,bullets, True, True):
            score+=1
            enemy = Enemy('ufo.png', randint(0, 920), 0, 80, 80, randint(2,4), 0)
            enemies.add(enemy)


player = Hero('rocket.png', 460, 600, 80, 100, 10, 0)
enemies = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy_1('asteroid.png', randint(0, 920), 0, 80, 80, randint(1,3), 0)
    asteroids.add(asteroid)
bullets = sprite.Group()

game = True
clock = time.Clock()

for i in range(1, 6):
    enemy = Enemy('ufo.png', randint(0, 920), 0, 80, 80, randint(2,4), 0)
    enemies.add(enemy)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(fon, (0,0))
    score_text=font.render('Счет:'+str(score), True, (255,255,255))
    miss_text=font.render('Пропущено:'+str(miss), True, (255,255,255))
    window.blit(score_text, (10,10))
    window.blit(miss_text, (10, 55))
    player.Control()
    player.reset()
    player.fire()
    bullets.draw(window)
    asteroids.draw(window)
    for asteroid in asteroids:
        asteroid.control_1()
    for enemy in enemies:
        enemy.control_1()
        enemy.death()
    enemies.draw(window)
    for bullet in bullets:
        bullet.arrive()
    if r == True:
        global start_t
        end_t = int(Time.time())
        if end_t-player.start_t >= 1 :
            r = False
            ammo = 30
        else:
            r = True
    if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False) or score>=30 or miss>=3:
        player.stop()
        for enemy in enemies:
            enemy.stop()
        for bullet in bullets:
            bullet.stop()
            bullet.kill()
        for asteroid in asteroids:
            asteroid.stop()
        finish = True
        if score < 30:
            text_lose = font.render('You lose', True, (255,255,255))
            window.blit(text_lose, (500,300))
        else:
            text_win = font.render('You win', True, (255,255,255))
            window.blit(text_win, (500,300))
    display.update()
    clock.tick(60)
