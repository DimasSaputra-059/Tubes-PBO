import math  #Modul math untuk melakukan operasi matematika
import pygame, sys #Modul yang menjadi dasar dari game, berperan sebagai class parent
import random #Modul random untuk mengacak posisi musuh
import image #Modul yang berisi file gambar
import sound #Modul sound untuk mengatur suara melalui file sound
from helper import draw_text
import abc

#fitur pembangun game
FPS=60
WIDTH=500
HEIGHT=600
GREEN = (0, 255, 0)

# Implementasi Inheritance
#class pygame (Class Utama/Parent)
pygame.init()
layar = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Galactic War")
fps = pygame.time.Clock()

#Class Player(Class Child)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Informasi dasar/awal seputar player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.player,(80,75))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 8
        self.score_val = 0
        self.life = 5
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 350
        self.shoot_speed = 0

    #artibuted movement
    def update(self): # Fungsi untuk mengatur durasi palyer menerima bonus
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000: # durasi palyer menerima bonus power per satuan milidetik
            self.power -= 1 
            self.power_time = pygame.time.get_ticks()
        
        if self.shoot_speed >= 1 and pygame.time.get_ticks() - self.speed_time > 10000:# durasi palyer menerima speed power per satuan milidetik
            self.shoot_speed -= 1
            self.shoot_delay += 250 # Mengembalikan delay shoot seperti semula ketika bonus berakhir
            self.speed_time = pygame.time.get_ticks()
            
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top  = 0

    def powerup(self): # fungsi untuk mengatur manfaat bonus power
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    
    def heal(self): # fungsi untuk mengatur manfaat bonus heal
        self.life += 1 # Menmbah nyawa player
    
    def speed_shoot(self): # fungsi untuk mengatur manfaat bonus speed
        self.shoot_speed += 1
        self.shoot_delay -= 250 # mempercepat delay saat menembak 
        self.speed_time = pygame.time.get_ticks()

    def shoot(self): # fungsi untuk mengatur tembakan palyer
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1: # Player akan menembakkan 1 bullet/peluru
                bullet = Bullet(pygame.Vector2(self.rect.centerx,self.rect.top))
                all_sprites.add(bullet)
                bullets.add(bullet)
                sound.missile.play()
            elif self.power >= 2: # Player akan menembakkan 2 bullet/peluru
                bullet1 = Bullet(pygame.Vector2(self.rect.centerx-20,self.rect.top))
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(pygame.Vector2(self.rect.centerx+20,self.rect.top))
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                sound.missile.play()  

    def show_lifepoints(self): # fungsi untuk menampilkan informasi score life point/ darah
        draw_text(layar, f"life points -> {self.life}", 15, WIDTH-70, HEIGHT-590)

    def show_score(self): # Fungsi untuk menampilkan informasi score 
        draw_text(layar, f"Score -> {self.score_val}", 15, WIDTH-450, HEIGHT-590)

# Implementasi Polymorphisme
#Class Alien(Class Child dari class pygame)
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.alien,(43,42))
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-50,-10)
        self.speedx=random.randrange(-1,1)
        self.speedy=random.randrange(1,2)
    #Atributed movement
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(-2,4)

#Class  Rock (Class child dari class pygame)
class Rock(Alien):
    def __init__(self):
        super().__init__()
        self.image=pygame.transform.scale(image.rock,(75,75))
        self.speedy=3

# Implemntasi Abstrakmethode
# Class Bonus (Class childe dari class pygame)
class Bonus(abc.ABC, pygame.sprite.Sprite):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

# Class Power (Class child dari pygame)
class Power(Bonus):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.power,(50,50))
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Class HealUP (Class child dari pygame)
class HealUP(Bonus):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.heal,(40,40))
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Class SpeedShoot (Class child dari pygame)
class SpeedShoot(Bonus):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.speed,(20,25))
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

#Class Bullet(Class Child dari class pygame)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,position:pygame.Vector2,angle:float=-90):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.rotate(pygame.transform.scale(image.bullet,(10,50)),-angle+180+90)
        self.rect=self.image.get_rect()
        self.rect.midbottom=position
        speedy = 10
        self.velocity = pygame.math.Vector2(math.cos(math.radians(angle))*speedy,math.sin(math.radians(angle))*speedy)

    def update(self):
        self.rect.midbottom += self.velocity
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

#Class Healthbar(Class Child dari class pygame)
class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH*4/5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 80

#Class Boss(Class Child dari class pygame)
class Boss(pygame.sprite.Sprite):
    def __init__(self, max_health:int, attack_speed:int = 50):
        # Baris kode mengatur posisi boss saat muncul
        pygame.sprite.Sprite.__init__(self)
        self.source_image = pygame.transform.rotate(pygame.transform.scale(image.boss,(200,180)),90)
        self._angle = 180
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 0

        # Informasi dasar/awal seputar boss
        self.max_health = max_health
        self._health = 0
        self.healthbar = Healthbar()
        self.health = self.max_health
        self.move_in = pygame.Vector2(0,15)
        all_sprites.add(self.healthbar)
        self.tick = 0
        self.alt = False
        self.attack_speed = attack_speed

    #Konsep Enkapsulasi (Setter dan Getter)
    @property
    def health(self): # fungsi getter health
        return self._health

    @health.setter
    def health(self, value): # fungsi setter health, beserta gambar bar darah boss
        self._health = value
        self.healthbar.image.fill((255,0 , 0))
        self.healthbar.image.fill((0, 255, 0), (0, 0, self.healthbar.image.get_width()*self.health/self.max_health, self.healthbar.image.get_height()))

    @property
    def angle(self): # fungsi getter angel/sudut
        return self._angle

    @angle.setter
    def angle(self, value): # fungsi getter angle/sudut
        if value != self._angle:
            self._angle = value
            self.on_angle_change()

    def on_angle_change(self): # fungsi untuk mengatur gerak boss ketika menembak player
        self.image = pygame.transform.rotate(self.source_image, self.angle)

    def hurt(self, value:int = 10): # fungsi untuk mengatur kalkulasi bar darah boss
        self.health -= value
        if self.health <= 0:
            self.kill()
            self.healthbar.kill()
 
    def shoot(self): # fungsi untuk mengatur sudut  rotasi tembakan boss
        self.alt = not self.alt
        if self.alt:
            bullet = Bullet(pygame.Vector2(self.rect.centerx-30,self.rect.bottom), -self.angle) 
        else :
            bullet = Bullet(pygame.Vector2(self.rect.centerx+30,self.rect.bottom), -self.angle)
        all_sprites.add(bullet)
        hazard.add(bullet)

    def update(self): # fungsi agar boss dapat menembak player secara otomatis
        self.rect.y += self.move_in.y
        if self.move_in.y > 0:
            self.move_in.y *= 0.95
        self.tick += 1

        p_center = player.rect.center
        s_center = self.rect.center
        angle_in_rads = math.atan2(p_center[1] - s_center[1], p_center[0] - s_center[0])

        self.angle = -math.degrees(angle_in_rads) 
        if self.tick > self.attack_speed:
            self.tick = 0
            self.shoot()

    def kill(self): # Fungsi ketika boss dikalahkan
        self.healthbar.kill()
        return super().kill()
        
#Fungsi tampilan kedua setelah menu() / Tampilan waiting
def waiting_screen():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "GALACTIC WAR!", 40, WIDTH/2, HEIGHT/4)
    draw_text(layar, "Arrow keys to move, Space key to fire", 20, WIDTH/2, HEIGHT/2)
    draw_text(layar, "Press any key to play", 22, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip() # Memperbarui tampilan setelah di update

    waiting = True # kondisi awal
    while waiting: # menu waiting berjalan
        fps.tick(FPS) #Menagtur kecepatan fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # game akan berakhir jika pada menu game over, user memilih quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP: # Menu waiting akan berakhir jika user mengklik tombol keyboard (manapun) 
                waiting = False

#Fungsi tampilan Menu game
def menu():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "GALACTIC WAR!", 50, WIDTH/2, HEIGHT/4)    
    pygame.display.flip() # Memperbarui tampilan setelah di update
    yvar=325
    xvar=250
    draw_text(layar, "START", 35, WIDTH/2, yvar-15) 
    draw_text(layar, "QUIT",40, WIDTH/2, 500)  
    pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
    
    waiting = True # Kondisi awal
    while waiting: # Layar menu berjalan
        fps.tick(FPS) #Mengatur kecepatan fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # game akan berakhir jika pada menu game over, user memilih quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # Jika tombol mouse ditekan, kode akan diajalnkan
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70: # Titik koordinat mouse, memulai game 
                    waiting = False # layar menu berhenti
                    waiting_screen() # layar waiting berjalan
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN: # Jika tombol mouse ditekan, kode akan diajalnkan
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (520 - ypos)**2)
                if cek <= 25: # Titik koordinat mouse,  game berakhir 
                    pygame.quit()
                    sys.exit()
        pygame.display.update() # Tampilan layar game akan di update sesuai perintah

#Fungsi tampilan menu ketika GameOver
def menuGameOver():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "Game Over", 50, WIDTH/2, HEIGHT/4)   
    yvar=350
    xvar=250
    draw_text(layar, "START", 35, WIDTH/2, yvar-15)
    draw_text(layar, f"Your score : {player.score_val}", 20, WIDTH/2, 223)
    draw_text(layar, "QUIT",40, WIDTH/2, 500) 
    pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
    
    waiting = True # Kondisi awal
    while waiting: # Layar game over berjalan
        fps.tick(FPS) # Mengatur kecepatan fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # game akan berakhir jika pada menu game over, user memilih quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # Jika tombol mouse ditekan, kode akan diajalnkan
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70: # Titik koordinat mouse, memulai game
                    player.score_val = 0 
                    waiting = False # Layar game over berhenti
            if event.type == pygame.MOUSEBUTTONDOWN: # Jika tombol mouse ditekan, kode akan diajalnkan
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (520 - ypos)**2)
                if cek <= 25: # Titik koordinat mouse, game berhenti/ditutup
                    pygame.quit()
                    sys.exit()
        pygame.display.update() # Tampilan layar game akan di update sesuai perintah

# Kondisi ketika game over terpenuhi
game_over = True
running=True # kondisi awal
hp = 0

# Tampilan awal menu
menu() 
sound.bgmusic.play(loops=-1) # Musik akan berputar tanpa henti (karena loops = -1)
while running: # layar menu berjalan
    fps.tick(FPS) #Menagtur kecepatan fps
    # waiting screen ketika gameover dan akan memulai game, game akan di reset untuk kembali seperti semula 
    if game_over:
        game_over = False
        # Kondisi awal game
        all_sprites = pygame.sprite.Group()
        hazard = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        level = 1
        all_sprites.add(player)

        # 3 Alien akan muncul setiap awal game
        for i in range(3):
            alien=Alien()
            all_sprites.add(alien)
            hazard.add(alien)
        player.score_val = 0

    for event in pygame.event.get():
        if event.type==pygame.QUIT: # game akan berakhir jika pada menu game over, user memilih quit
            running=False # layar menu berhenti
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE: # keyboard spasi untuk menembak
                player.shoot()
    all_sprites.update() # semua objek di update.

    hits=pygame.sprite.groupcollide(hazard,bullets,False,True)
    for hit in hits:
        # mengecek apakah peluru mengenai alien, jika kena maka alien akan kembali respawn
        if isinstance(hit, Alien):
            sound.exlp2.play()
            hit.kill()
            alien=Alien()
            all_sprites.add(alien)
            hazard.add(alien)
            player.score_val +=1 #jika peluru mengenai alien, skor bertambah 1

            #setiap skor kelipatan 100, HP Boss bertambah 50, 
            if player.score_val % 100 == 0:
                hp += 50 
                boss = Boss(hp)
                all_sprites.add(boss)
                hazard.add(boss)
                player.powerup()
                level += 1 #ketika boss dikalahkan, lv akan meningkat
                player.life += 1 #ketika boss dikalahkan, mendapat tambahan 1 hp

            #setiap skor kelipatan 20, Bonus power akan muncul
            elif player.score_val % 20 == 0:
                power=Power()
                all_sprites.add(power)
                hazard.add(power)
            
            #setiap skor kelipatan 75, Bonus heal akan muncul
            elif player.score_val % 75 == 0:
                heal=HealUP()
                all_sprites.add(heal)
                hazard.add(heal)
            
            #setiap skor kelipatan 35, Bonus speed akan muncul
            elif player.score_val % 35 == 0:
                speed=SpeedShoot()
                all_sprites.add(speed)
                hazard.add(speed)
             
            #setiap skor kelipatan 5, rintangan batu akan muncul
            elif player.score_val % 5 == 0:
                rock=Rock()
                all_sprites.add(rock)
                hazard.add(rock)

        # cek apakah peluru mengenai Rock        
        elif isinstance(hit, Rock):
            sound.exlp2.play()
            hit.kill()
            player.score_val += 0
            
        # cek apakah peluru mengenai Boss        
        elif isinstance(hit, Boss): 
            sound.exlp2.play()
            hit.hurt()
            
    # ketika level lebih dari 2, alien bergerak lebih cepat
    if level >= 2:
        alien.speedx=random.randrange(-3,1)
        alien.speedy=random.randrange(3,7)
        
    # Tampilan layar dalam permainan
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, f"Level {level}", 24, WIDTH/2, HEIGHT-590)
    all_sprites.draw(layar)
    player.show_score()
    player.show_lifepoints()
    pygame.display.update()

    hits = pygame.sprite.spritecollide(player,hazard,False,pygame.sprite.collide_circle)
    for hit in hits:
        # jika pesawat terkena hit Alien, life akan berkurang, dan alien yang hancur akan respawn
        if isinstance(hit, Alien):
            sound.expl.play()
            hit.kill()
            alien=Alien()
            all_sprites.add(alien)
            hazard.add(alien)
            player.life -= 1

        # jika pesawat terkena hit Rock (Batu), life akan berkurang
        elif isinstance(hit, Rock):
            sound.expl.play()
            hit.kill()
            player.life -= 1

        # jika pesawat terkena hit Bullet (Peluru) dari boss, life akan berkurang
        elif isinstance(hit, Bullet):
            sound.expl.play()
            hit.kill()
            player.life -= 1

        # jika pesawat mengambil bonus power, player akan memperoleh manfaat bonus
        elif isinstance(hit, Power):
            hit.kill()
            sound.powerup.play()
            player.powerup()

        # jika pesawat mengambil bonus SpeedShoot, player akan memperoleh manfaat bonus
        elif isinstance(hit, SpeedShoot):
            hit.kill()
            sound.speedup.play()
            player.speed_shoot()

        # jika pesawat mengambil bonus heal, player akan memperoleh manfaat bonus
        else :
            hit.kill()
            sound.heal.play()
            player.heal()
        
        # Jika life (Nyawa) player habis, game akan berakhir dan menampilkan menu game over
        if player.life < 0:
            game_over = True
            menuGameOver()     

# Game berakhir   
pygame.quit()
