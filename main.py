import pygame as pg
import random as ran

pg.init()  # Inisialisasi pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Konfigurasi ukuran jendela game
pg.display.set_caption("Perang Layangan")  # Konfigurasi nama jendela game

# Memanggil file gambar background
background_image = pg.image.load(".\\assets\\images\\Clouds5\\1.png")  
moon_sprite = pg.image.load(".\\assets\\images\\Clouds5\\2.png")  
cloud1_sprite = pg.image.load(".\\assets\\images\\Clouds5\\4.png")  
cloud2_sprite = pg.image.load(".\\assets\\images\\Clouds5\\5.png")  
cloud_moving_sprite = pg.image.load(".\\assets\\images\\Clouds5\\3.png")  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Mengubah resolusi gambar sesuai ukuran jendela game
background_image = pg.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  
moon_sprite = pg.transform.scale(moon_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud1_sprite = pg.transform.scale(cloud1_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud2_sprite = pg.transform.scale(cloud2_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  
cloud_moving_sprite = pg.transform.scale(cloud_moving_sprite, (SCREEN_WIDTH, SCREEN_HEIGHT))  

cloud_moving_x = -cloud_moving_sprite.get_width()  
cloud_moving_y = ran.randint(0, 100)
cloud_speed = 1  # Kecepatan gerak gambar awan

bgm = pg.mixer.Sound(".\\assets\\music\\menu_music.mp3")  # Memanggil file musik
bgm.set_volume(0.5)
bgm.play(-1)  # Memainkan musik secara loop

game_over_sound = pg.mixer.Sound(".\\assets\\music\\game_over.mp3")
wind_sound = pg.mixer.Sound(".\\assets\\music\\wind_sound.mp3")

game_state = "start_menu"  # Atur game_state ke "start_menu"


# # Menambahkan variabel untuk misi
# mission_target = 5  # Jumlah layangan musuh yang harus dipotong
# mission_time_limit = 30  # Batas waktu misi dalam detik
# time_remaining = mission_time_limit  # Waktu yang tersisa
# enemies_cut = 0  # Jumlah layangan musuh yang dipotong

# Memanggil file sprite layangan    
layangan_image = [
    pg.image.load(".\\assets\\images\\layangan1.png"),
    pg.image.load(".\\assets\\images\\layangan2.png"),
    pg.image.load(".\\assets\\images\\layangan3.png"),
    pg.image.load(".\\assets\\images\\layangan4.png")
]  # Memanggil file sprite layangan

layangan_selected = 0  # Layangan Default

def draw_kite_selection():
    font = pg.font.SysFont('arial', 40)
    select_text = font.render('Pilih Layangan', True, (BLACK))
    left_arrow = font.render('<', True, (BLACK))
    right_arrow = font.render('>', True, (BLACK))
    start_text = font.render('Tekan Spasi untuk Mulai', True, (BLACK))

    # Tampilkan pilihan layangan
    kite_image = layangan_image[layangan_selected]
    kite_image = pg.transform.scale(kite_image, (150, 150))

    screen.blit(select_text, (SCREEN_WIDTH / 2 - select_text.get_width() / 2, SCREEN_HEIGHT / 4))
    screen.blit(left_arrow, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    screen.blit(kite_image, (SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 75))
    screen.blit(right_arrow, (SCREEN_WIDTH - SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    screen.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, SCREEN_HEIGHT / 1.5))

    pg.display.update()

def draw_start_menu():
    font = pg.font.SysFont('arial', 40)
    title = font.render('Perang Layangan', True, (BLACK))
    start_button = font.render('Mulai', True, (BLACK))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 2 - 20))
    screen.blit(start_button, (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT / 2 + start_button.get_height() / 2 + 20))
    pg.display.update()

def draw_game_over_screen():  # Fungsi untuk menampilkan menu game over
    font = pg.font.SysFont('arial', 40)
    title = font.render('GAME OVER', True, (BLACK))
    restart_button = font.render('R - Restart', True, (BLACK))
    quit_button = font.render('Q - Quit', True, (BLACK))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/4 - title.get_height()/3))
    screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
    pg.display.update()


# def draw_mission_status():
#     font = pg.font.SysFont('arial', 24)
#     mission_text = font.render(f'Potong {mission_target} layangan musuh!', True, (BLACK))
#     time_text = font.render(f'Waktu Tersisa: {time_remaining:.1f} detik', True, (BLACK))
#     enemies_cut_text = font.render(f'Layangan Musuh Dipotong: {enemies_cut}/{mission_target}', True, (BLACK))
    
#     screen.blit(mission_text, (10, 40))
#     screen.blit(time_text, (10, 70))
#     screen.blit(enemies_cut_text, (10, 100))

def handle_collisions(player, enemies):
    for enemy in enemies:
        if enemy.check_collision(player):  # Periksa tabrakan antara musuh dan pemain
            return True  # Game over jika terjadi tabrakan
    return False  # Game masih berlanjut

class Player(pg.sprite.Sprite):
    def __init__(self, image, x, y, speed=5, gravity=1.0, jump_strength=-10, max_jumps=2, health=100):
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
        self.health = health  # Tambahkan atribut kesehatan

        self.wind_speed = 0
        self.wind_direction = 0

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
        if self.rect.y >= SCREEN_HEIGHT - 100:  # Batas tanah
            self.rect.y = SCREEN_HEIGHT - 100
            self.vertical_velocity = 0
            self.jumps_left = self.max_jumps  # Reset lompatan saat menyentuh tanah
            self.is_jumping = False  # Kembali ke posisi tidak melompat

    def update(self, mouse_pos):
        # Efek gravitasi
        self.apply_gravity()

        # Mengatur arah layangan berdasarkan posisi mouse
        if mouse_pos[0] < self.rect.centerx:  # Jika mouse berada di kiri layangan
            self.facing_left = True
        else:  # Jika mouse berada di kanan layangan
            self.facing_left = False

        # Horizontal movement ketika melompat
        if self.vertical_velocity != 0:
            if self.facing_left:
                self.rect.x -= self.horizontal_jump_speed
            else:
                self.rect.x += self.horizontal_jump_speed
        
        # Menambahkan logika untuk angin
        self.rect.x += self.wind_speed * self.wind_direction  # Menggerakkan layangan berdasarkan angin
        if ran.random() < 0.01:  # Ada peluang 1% untuk mengaktifkan angin setiap frame
            self.wind_speed = ran.randint(1, 5)  # Atur kecepatan angin
            self.wind_direction = ran.choice([-1, 1])  # Pilih arah angin (kiri atau kanan)
        else:
            self.wind_speed = max(0, self.wind_speed - 0.1)  # Tidak ada angin
        
        # Membatasi gerakan dalam batas jendela
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

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
    
    # Fungsi untuk mengurangi nyawa
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return True  # Player mati
        return False  # Player masih hidup

    def draw_health(self, screen):
        font = pg.font.SysFont('arial', 24)
        if self.health > 30:
            health_text = font.render(f'Health: {self.health}', True, (GREEN))
        else:
            health_text = font.render(f'Health: {self.health}', True, (RED))
        screen.blit(health_text, (10, 10))  # Tampilkan nyawa di sudut kiri atas

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

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):  # Periksa tabrakan
            if player.take_damage():  # Jika pemain mati
                return True  # Tanda bahwa game over
        return False  # Masih hidup

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Menggambar musuh ke layar

# Player and enemies initialization
player = Player(layangan_image[layangan_selected], SCREEN_WIDTH//2, SCREEN_HEIGHT//3)  # Initial position
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

        if game_state == "kite_selection":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:  # Pindah ke layangan sebelumnya
                    layangan_selected = (layangan_selected - 1) % len(layangan_image)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:  # Pindah ke layangan berikutnya
                    layangan_selected = (layangan_selected + 1) % len(layangan_image)
                elif event.key == pg.K_SPACE:  # Konfirmasi pilihan dan mulai game
                    player = Player(layangan_image[layangan_selected], SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    game_state = "playing"

    if game_state == "kite_selection":
        draw_kite_selection()  # Terus gambar layangan di setiap frame
        
        # Update semua musuh
        # enemies.update()
        if game_state == "game_over":
            draw_game_over_screen()  # Gambar layar game over

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        # Restart game
                        player = Player(layangan_image[layangan_selected], SCREEN_HEIGHT//2, SCREEN_WIDTH//2)  # Reset player
                        enemies.empty()  # Hapus semua musuh
                        # Tambahkan musuh baru
                        for _ in range(5):
                            enemy = Enemy(layangan_image[ran.randint(0, 3)])
                            enemies.add(enemy)
                        game_state = "playing"  # Kembali ke permainan
                    elif event.key == pg.K_q:
                        pg.quit()

    # Kontrol untuk pemain
    if game_state == "playing":
        wind_sound.play(-1)
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        # Jika ingin menggunakan keyboard
        # if keys[pg.K_LEFT] or keys[pg.K_a]:
        #     player.move_left()
        #     player.facing_left = True  # Update arah pemain
        # if keys[pg.K_RIGHT] or keys[pg.K_d]:
        #     player.move_right()
        #     player.facing_left = False  # Update arah pemain
        if keys[pg.K_SPACE] or keys[pg.K_w]:
            player.jump()  # Melompat jika spasi ditekan
        else:
            player.is_jumping = False  # Set pemain tidak dalam keadaan melompat jika spasi tidak ditekan

        # Update dan gambar player
        player.draw(screen)  # Gambar pemain
        player.update(mouse_pos)  # Pembaruan posisi pemain menggunakan mouse mouse
        enemies.draw(screen)  # Gambar semua musuh
        enemies.update()  # Pembaruan status musuh
        player.draw_health(screen)  # Gambar kesehatan pemain
        # draw_mission_status()

            # Periksa tabrakan
        if handle_collisions(player, enemies):
            game_state = "game_over"
            game_over_sound.play()
        
        # # Hitung waktu yang tersisa untuk misi
        # if time_remaining > 0:
        #     time_remaining -= clock.tick(60) / 100  # Kurangi waktu berdasarkan frame rate
        # else:
        #     game_over_sound.play()  # Suara game over
        #     game_state = "game_over"

    pg.display.flip()  # Perbarui layar

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
        # time_remaining = mission_time_limit
        draw_start_menu()
        if keys[pg.K_SPACE]:
            game_state = "kite_selection"
    elif game_state == "game_over":
        draw_game_over_screen()  # Menggambar layar game over
        if keys[pg.K_r]:
            game_state = "start_menu"
        if keys[pg.K_q]:
            pg.quit()
            quit()

    pg.display.update()  # Refresh layar

pg.quit()  # Menghentikan pygame
