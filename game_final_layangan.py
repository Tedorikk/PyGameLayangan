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

class Layangan:
    def __init__(self, image, x, y, speed=15, gravity=1.0, jump_strength=-10, max_jumps=2):
        self.image = pg.transform.scale(image, (50, 50))
        self.x = x
        self.y = y
        self.speed = speed
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.vertical_velocity = 0
        self.facing_left = True
        self.on_ground = True
        self.horizontal_jump_speed = 5
        self.jump_cooldown = 250
        self.last_jump_time = 0
        self.jumps_left = max_jumps  # Jumlah lompatan tersisa yang diizinkan
        self.max_jumps = max_jumps  # Lompatan maksimal sebelum menyentuh tanah
    
    def move_left(self, dt):
        self.facing_left = True
        self.x -= self.speed * dt / 1000

    def move_right(self, dt):
        self.facing_left = False
        self.x += self.speed * dt / 1000

    def jump(self):
        current_time = pg.time.get_ticks()
        if self.jumps_left > 0 and current_time - self.last_jump_time > self.jump_cooldown:
            self.vertical_velocity = self.jump_strength
            self.last_jump_time = current_time
    
    def apply_gravity(self):
        self.vertical_velocity += self.gravity
        self.y += self.vertical_velocity
        if self.y >= 550:  # Ground limit
            self.y = 550
            self.vertical_velocity = 0
            self.on_ground = True
            self.jumps_left = self.max_jumps  # Reset lompatan saat menyentuh tanah
        else:
            self.on_ground = False
    
    def update(self, dt):
        # Gravity effect
        self.apply_gravity()

        # Horizontal movement when jumping
        if self.vertical_velocity != 0:
            if self.facing_left:
                self.x -= self.horizontal_jump_speed * dt / 100
            else:
                self.x += self.horizontal_jump_speed * dt / 100

    def draw(self, screen):
        # Flip image if facing left
        image_to_draw = pg.transform.flip(self.image, True, False) if self.facing_left else self.image
        screen.blit(image_to_draw, (self.x, self.y))


# Player and enemy initialization using Layangan class
player = Layangan(layangan_image[layangan_selected], 200, 400)  # Initial position
enemy = Layangan(layangan_image[ran.randint(0, 3)], 600, 400)  # Random enemy
enemy_direction = 1  # 1 for right, -1 for left

running = True

# Clock pygame
clock = pg.time.Clock()

while running:
    dt = clock.tick(60)  # Mengatur game berjalan pada 60 FPS dan mendapatkan waktu yang berlalu sejak frame terakhir
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Gambar background
    screen.blit(background_image, (0, 0))  # Menampilkan gambar background di lapisan paling bawah
    screen.blit(moon_sprite, (0, 0))  # Menampilkan gambar bulan satu lapisan diatas gambar latar belakang
    screen.blit(cloud1_sprite, (0, 0))  # Menampilkan gambar awan lapisan bawah satu lapisan diatas gambar bulan
    screen.blit(cloud2_sprite, (0, 0))  # Menampilkan gambar awan lapisan atas satu lapisan diatas gambar awan lapisan bawah

    cloud_moving_x += cloud_speed  # Menggerakkan awan ke kanan

    if cloud_moving_x > SCREEN_WIDTH:  # Jika awan keluar layar, awan kembali ke awal
        cloud_moving_x = -cloud_moving_sprite.get_width()
        cloud_moving_y = ran.randint(0, 100)

    # Menampilkan gambar awan bergerak
    screen.blit(cloud_moving_sprite, (cloud_moving_x, cloud_moving_y))

    # Panggil fungsi untuk menggambar menu
    keys = pg.key.get_pressed()
    if game_state == "start_menu":
        draw_start_menu()
        if keys[pg.K_SPACE]:
            player.x, player.y = (SCREEN_WIDTH//2), SCREEN_HEIGHT//2
            game_state = "game"
            game_over = False
    elif game_state == "game_over":
        draw_game_over_screen()
        if keys[pg.K_r]:
            game_state = "start_menu"
        if keys[pg.K_q]:
            pg.quit()
            quit()
    elif game_state == "game":
        # Gerakan kiri dan kanan menggunakan keyboard untuk player
        if keys[pg.K_LEFT]:
            player.move_left(dt)
        if keys[pg.K_RIGHT]:
            player.move_right(dt)

        # Lompatan
        if keys[pg.K_SPACE]:
            player.jump()  # Memanggil fungsi lompatan jika tombol spasi ditekan

        # Update posisi dan gerakan player
        player.update(dt)

        # Gerakan acak musuh
        enemy.x += enemy_direction * 3  # Gerakan musuh
        if enemy.x < 0 or enemy.x > SCREEN_WIDTH - enemy.image.get_width():  # Bounce back
            enemy_direction *= -1  # Ubah arah gerakan musuh
        enemy.update(dt)  # Update enemy

        # Deteksi kolisi antara player dan enemy
        if (player.x < enemy.x + enemy.image.get_width() and
            player.x + player.image.get_width() > enemy.x and
            player.y < enemy.y + enemy.image.get_height() and
            player.y + player.image.get_height() > enemy.y):
            game_state = "game_over"  # Set game state to game over jika terjadi kolisi

        # Gambar player dan musuh
        player.draw(screen)
        enemy.draw(screen)

    pg.display.update()  # Update tampilan game

pg.quit()  # Keluar dari game
