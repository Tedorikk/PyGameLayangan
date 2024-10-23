import pygame as pg
import random as ran

pg.init()  # Inisialisasi pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Konfigurasi ukuran jendela game
pg.display.set_caption("Perang Layangan")  # Konfigurasi nama jendela game

# Memanggil file gambar background
background_image = pg.image.load("Clouds5/1.png")  
moon_sprite = pg.image.load("Clouds5/2.png")  
cloud1_sprite = pg.image.load("Clouds5/4.png")  
cloud2_sprite = pg.image.load("Clouds5/5.png")  
cloud_moving_sprite = pg.image.load("Clouds5/3.png")  

# Mengubah resolusi gambar sesuai ukuran jendela game
background_image = pg.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  
moon_sprite = pg.transform.scale(moon_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud1_sprite = pg.transform.scale(cloud1_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud2_sprite = pg.transform.scale(cloud2_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud_moving_sprite = pg.transform.scale(cloud_moving_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  

cloud_moving_x = -cloud_moving_sprite.get_width()  
cloud_moving_y = ran.randint(0, 100)
cloud_speed = 1  # Kecepatan gerak gambar awan

pg.mixer.music.load("menu_music.mp3")  # Memanggil file musik
pg.mixer.music.play(-1)  # Memainkan musik secara loop

game_state = "start_menu"  # Atur game_state ke "start_menu"

def draw_start_menu():  # Fungsi untuk menampilkan menu awal
    font = pg.font.SysFont('arial', 40)
    title = font.render('Perang Layangan', True, (49, 76, 102))
    start_button = font.render('Mulai', True, (49, 76, 102))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 2 - 20))
    screen.blit(start_button, (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT / 2 + start_button.get_height() / 2 + 20))
    pg.display.update()

def draw_game_over_screen():  # Fungsi untuk menampilkan menu game over
    screen.fill((0, 0, 0))
    font = pg.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (255, 255, 255))
    restart_button = font.render('R - Restart', True, (255, 255, 255))
    quit_button = font.render('Q - Quit', True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/3))
    screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
    pg.display.update()

layangan_image = [
    pg.image.load("layangan1.png"),
    pg.image.load("layangan2.png"),
    pg.image.load("layangan3.png"),
    pg.image.load("layangan4.png")
]  # Memanggil file sprite layangan

layangan_selected = 0  # Layangan Default

class Player(pg.sprite.Sprite):
    def __init__(self, image, x, y, speed=15, gravity=1.0, jump_strength=-10, max_jumps=2):
        super().__init__()
        self.image = pg.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.vertical_velocity = 0
        self.facing_left = True
        self.horizontal_jump_speed = 5
        self.jump_cooldown = 250
        self.last_jump_time = 0
        self.jumps_left = max_jumps  # Jumlah lompatan tersisa yang diizinkan
        self.max_jumps = max_jumps  # Lompatan maksimal sebelum menyentuh tanah
        self.is_jumping = False  # Menandai jika pemain sedang melompat

    def jump(self):
        # Hanya melompat jika spasi ditekan dan masih bisa melompat
        if self.jumps_left > 0 and not self.is_jumping:
            self.vertical_velocity = self.jump_strength
            self.is_jumping = True  # Set pemain dalam keadaan melompat

    def apply_gravity(self):
        # Terus menerapkan gravitasi
        self.vertical_velocity += self.gravity
        self.rect.y += self.vertical_velocity
        
        # Reset jika menyentuh tanah
        if self.rect.y >= 550:  # Batas tanah
            self.rect.y = 550
            self.vertical_velocity = 0
            self.jumps_left = self.max_jumps  # Reset lompatan saat menyentuh tanah
            self.is_jumping = False  # Kembali ke posisi tidak melompat

    def update(self):
        # Efek gravitasi
        self.apply_gravity()

        # Horizontal movement ketika melompat
        if self.vertical_velocity != 0:
            if self.facing_left:
                self.rect.x -= self.horizontal_jump_speed
            else:
                self.rect.x += self.horizontal_jump_speed

    def move_left(self):
        self.rect.x -= self.speed
        # Batas jendela kiri
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.speed
        # Batas jendela kanan
        if self.rect.x > SCREEN_WIDTH - self.image.get_width():
            self.rect.x = SCREEN_WIDTH - self.image.get_width()

    def draw(self, screen):
        # Flip image if facing left
        image_to_draw = pg.transform.flip(self.image, True, False) if self.facing_left else self.image
        screen.blit(image_to_draw, self.rect.topleft)

class Enemy(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pg.transform.scale(image, (50, 50))  # Mengubah ukuran gambar
        self.rect = self.image.get_rect()
        self.rect.y = ran.randint(0, SCREEN_HEIGHT - 75)  # Posisi acak untuk y
        self.speed = ran.randint(1, 5)  # Kecepatan acak

        # Tentukan arah awal: 1 untuk ke kanan, -1 untuk ke kiri
        self.direction = ran.choice([-1, 1])
        if self.direction == 1:  # Jika bergerak ke kanan
            self.rect.x = -self.image.get_width()  # Muncul dari kiri
        else:  # Jika bergerak ke kiri
            self.rect.x = SCREEN_WIDTH  # Muncul dari kanan

    def update(self):
        self.rect.x += self.speed * self.direction  # Menggerakkan musuh secara horizontal

        # Jika musuh keluar layar, reset posisi
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.reset_position()

    def reset_position(self):
        # Mengatur ulang posisi x dan y untuk kemunculan kembali
        self.rect.y = ran.randint(0, SCREEN_HEIGHT - 75)  # Posisi y acak
        self.direction *= -1  # Ubah arah bergerak

        # Jika bergerak ke kanan, mulai dari kiri; jika ke kiri, mulai dari kanan
        if self.direction == 1:
            self.rect.x = -self.image.get_width()  # Muncul dari kiri
        else:
            self.rect.x = SCREEN_WIDTH  # Muncul dari kanan
        self.speed = ran.randint(5, 10)  # Kecepatan acak untuk gerakan berikutnya

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Menggambar musuh ke layar

# Player and enemies initialization
player = Player(layangan_image[layangan_selected], 200, 400)  # Initial position
enemies = pg.sprite.Group()  # Mengelompokkan semua musuh

# Menambahkan beberapa musuh ke dalam kelompok enemies
enemies = pg.sprite.Group()
# Menambahkan beberapa musuh
for _ in range(5):  # Menambahkan 5 musuh
    enemy = Enemy(layangan_image[ran.randint(0, 3)])
    enemies.add(enemy)

running = True

# Clock pygame
clock = pg.time.Clock()

while running:
    dt = clock.tick(60)  # Mengatur game berjalan pada 60 FPS dan mendapatkan waktu yang berlalu sejak frame terakhir
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Update semua musuh
        enemies.update()
        # Memeriksa tombol untuk restart atau quit
        if game_state == "game_over":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    # Restart game
                    player = Player(layangan_image[layangan_selected], 200, 400)  # Reset player
                    enemies.empty()  # Hapus semua musuh
                    # Tambahkan musuh baru
                    for _ in range(5):
                        # Menambahkan beberapa musuh
                        enemy = Enemy(layangan_image[ran.randint(0, 3)])
                        enemies.add(enemy)
                    game_state = "playing"  # Kembali ke state bermain
                elif event.key == pg.K_q:
                    running = False

        # Kontrol untuk pemain
        if game_state == "playing":
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                player.move_left()
                player.facing_left = True  # Update arah pemain
            if keys[pg.K_RIGHT]:
                player.move_right()
                player.facing_left = False  # Update arah pemain
            if keys[pg.K_SPACE]:
                player.jump()  # Melompat jika spasi ditekan
            else:
                player.is_jumping = False  # Set pemain tidak dalam keadaan melompat jika spasi tidak ditekan

    # Pembaruan status permainan
    if game_state == "playing":
        player.update()  # Pembaruan status pemain
        enemies.update()  # Pembaruan status musuh

        # Cek tabrakan antara pemain dan musuh
        if pg.sprite.spritecollideany(player, enemies):
            game_state = "game_over"  # Ubah state permainan ke game over

    # Menggambar semua elemen di layar
    screen.blit(background_image, (0, 0))  # Menggambar latar belakang
    screen.blit(cloud1_sprite, (0, 0))  # Menggambar awan statis
    screen.blit(cloud2_sprite, (0, 0))  # Menggambar awan statis

    # Menggambar awan bergerak
    cloud_moving_x += cloud_speed
    if cloud_moving_x > SCREEN_WIDTH:
        cloud_moving_x = -cloud_moving_sprite.get_width()  # Reset posisi awan saat keluar layar
    screen.blit(cloud_moving_sprite, (cloud_moving_x, cloud_moving_y))  # Menggambar awan yang bergerak

    player.draw(screen)  # Menggambar pemain
    enemies.draw(screen)  # Menggambar musuh

    # Menampilkan menu awal
    keys = pg.key.get_pressed()
    if game_state == "start_menu":
        draw_start_menu()
        if keys[pg.K_SPACE]:
            game_state = "playing"
    elif game_state == "game_over":
        draw_game_over_screen()  # Menggambar layar game over
        if keys[pg.K_r]:
            game_state = "start_menu"
        if keys[pg.K_q]:
            pg.quit()
            quit()

    pg.display.update()  # Refresh layar

pg.quit()  # Menghentikan pygame
