from pygame import*
from random import randint
from time import time as timer

 
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = 3
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
       
       
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed+10
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed+10
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)   
        bullets.add(bullet)
        pass
lost = 0
font.init()
font1  = font.SysFont('Arial', 40)
font2  = font.SysFont('Arial', 40)
bullets = sprite.Group()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,420)
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("SPACE")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
win = font2.render('U WIN!', True, (255, 215, 0))
lose = font2.render('U LOPUX!', True, (255, 215, 0))
 
#Персонажи игры:
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

w =0 

#final = GameSprite('asteroid.png', win_width - 120, win_height - 80, 0)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width- 80),
    -40,80, 50, randint(1, 5))
    monsters.add(monster)
game = True
clock = time.Clock()
FPS = 60
 
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound("fire.ogg")
asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy('asteroid.png', randint(80, win_width- 80), -40,80, 50, randint(1, 5))
    asteroids.add(asteroid)

                    

num_fire = 0
rel_time = False

finish = False


while game:
    
    for e in event.get():
        if e.type == QUIT:
                
            game = False
            monsters.draw(window)
            monsters.update()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time=timer()
                    rel_time=True
                    

                    
    if not finish:
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render('Wait,reload',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
                
        collides = sprite.groupcollide(
                            monsters, bullets, True, True     
                        )
        for c in collides:
            w += 1
            monster = Enemy('ufo.png', randint(80, win_width- 80), -40,80, 50, randint(1, 5))
            monsters.add(monster)
            
            
        window.blit(background,(0, 0)) 
                                
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255)) 
        text_w = font1.render("Счет: " + str(w), 1, (255, 255, 255))       
        window.blit(text_lose,(10, 50))
        window.blit(text_w,(10, 25))
                                
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)


                                #final.reset()
        monsters.update()
        ship.update()
        bullets.update()
                            
        if w >= 5:
            finish = True
            window.blit(win,(200,200))
        if lost >= 9:
            finish = True
            window.blit(lose,(200,200))
    display.update()
    clock.tick(FPS)

