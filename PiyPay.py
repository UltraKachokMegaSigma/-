from pygame import*
import random
#

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet= "bullet.png"
img_ast = "asteroid.png"

#
score = 0
lost = 0
life = 3
max_lost = 4
max_score = 15

#
win_w = 700
win_h = 500

#
window = display.set_mode((win_w, win_h))
#
background = transform.scale(image.load(img_back),(win_w, win_h))

#
#
class GameSprite(sprite.Sprite):
    #
    def __init__(self,player_image, player_x,player_y,size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)
        #
        self.image = transform.scale(image.load(player_image),(50,60))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

        #
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
#
class Player(GameSprite):
    def update(self):

        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        #
        #
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 5,7,-20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.y = 0
            self.rect.x = random.randint(80,win_w - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Rock(GameSprite):
    def update(self):
        self.rect.y += self.speed #
        global lost
        if self.rect.y > win_h:
            spawn_chance = random.randint(1, 100)
            if spawn_chance <=5: #
                self.rect.y = -10
                self.rect.x = random.randint(50, win_w - 80)


#
ship = Player(img_hero, 5, win_h -100, 80,100,10)
#
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, random.randint(80,win_w - 80), -40,80,30, random.randint(2,5))
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Rock(img_ast, random.randint(80,win_w - 80), -40,80,30, random.randint(2,5))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render("You WIN!",True,(255,255,255))
lose = font1.render("You LOSE!",True,(180,0,0))

finish = False
run = True

def restart_game():
    global score, lost, life, finish

    #
    score = 0
    lost = 0
    life = 3
    finish = False

    ship.rect.x = 5
    ship.rect.x = win_h - 100
    monsters.empty()
    bullets.empty()

    for i in range(1, 6):
        monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 30, random.randint(2, 5))
        monsters.add(monster)

    for i in range(1, 3):
        asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80, 30, random.randint(2, 5))
        asteroids.add(asteroid)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
            elif e.key == K_RETURN and finish:
                restart_game()

    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Рахунок:" +str(score), 1,(255,255,255))
        window.blit(text, (10, 10))

        text_lose = font2.render(":" +str(lost), 1,(180,0,0))
        window.blit(text_lose, (10, 300))

        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, random.randint(80, win_w - 80), -40, 80, 30, random.randint(2, 5))
            monsters.add(monster)

        collides2 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides2:
            score = score + 3
            asteroid = Rock(img_ast, random.randint(80, win_w - 80), -40, 80, 30, random.randint(2, 5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, False):
            for c in sprite.spritecollide(ship, monsters, False):
                c.rect.x = random.randint(80, win_w-80)
                c.rect.y = -40
                life = life - 1

        elif sprite.spritecollide(ship, asteroids, False):
            for c in sprite.spritecollide(ship, asteroids, False):
                c.rect.x = random.randint(80, win_w-80)
                c.rect.y = -40
                life = life - life

        if life ==0 or lost >= max_lost:
            finish = False
            window.blit(lose, (200, 200))

        if score >= max_score:
            finish = True
            window.blit(lose, (200, 200))
        display.update()

    time.delay(50)



















