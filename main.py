import pygame as pg
import random as ran

pg.init()  # Inisialisasi pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Konfigurasi ukuran jendela game
pg.display.set_caption("Perang Layangan")  # Konfigurasi nama jendela game

# Memanggil file gambar background
background_image = pg.image.load(".\\assets\\images\\Morning\\1.png")
moon_sprite = pg.image.load(".\\assets\\images\\Morning\\2.png")  
cloud1_sprite = pg.image.load(".\\assets\\images\\Morning\\4.png")  
cloud2_sprite = pg.image.load(".\\assets\\images\\Morning\\5.png")  
cloud_moving_sprite = pg.image.load(".\\assets\\images\\Morning\\3.png")

# start_menu_image = pg.image.load(".\\assets\\images\\Other\\menu.jpg")

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

# start_menu_image = pg.transform.scale(start_menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

cloud_moving_x = -cloud_moving_sprite.get_width()  
cloud_moving_y = ran.randint(0, 100)
cloud_speed = 1  # Kecepatan gerak gambar awan

bgm = pg.mixer.Sound(".\\assets\\music\\menu_music.mp3")  # Memanggil file musik
bgm.set_volume(0.5)
bgm.play(-1)  # Memainkan musik secara loop

game_over_sound = pg.mixer.Sound(".\\assets\\music\\game_over.mp3")
game_over_sound.set_volume(1)
wind_sound = pg.mixer.Sound(".\\assets\\music\\wind_sound.mp3")
select_sound = pg.mixer.Sound(".\\assets\\music\\select.mp3")

game_state = "start_menu"  # Atur game_state ke "start_menu"

# Menambahkan variabel untuk misi
mission_target = 5  # Jumlah layangan musuh yang harus dipotong
mission_time_limit = 60  # Batas waktu misi dalam detik
time_remaining = mission_time_limit  # Waktu yang tersisa
enemies_cut = 0  # Jumlah layangan musuh yang dipotong

# Memanggil file sprite layangan    
layangan_image = [
    pg.image.load(".\\assets\\images\\layangan1.png"),
    pg.image.load(".\\assets\\images\\layangan2.png"),
    pg.image.load(".\\assets\\images\\layangan3.png"),
    pg.image.load(".\\assets\\images\\layangan4.png")
]  # Memanggil file sprite layangan

layangan_selected = 0  # Layangan Default

def draw_kite_selection():
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 40)
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
    # screen.blit(start_menu_image, (0, 0))
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 48)
    title = font.render('Perang Layangan', True, (BLACK))
    start_button = font.render('Mulai', True, (BLACK))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT / 2 - title.get_height() / 2 - 20))
    screen.blit(start_button, (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT / 2 + start_button.get_height() / 2 + 20))

def draw_game_over_screen():  # Fungsi untuk menampilkan menu game over
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 40)
    title = font.render('GAME OVER', True, (BLACK))
    restart_button = font.render('R - Restart', True, (BLACK))
    quit_button = font.render('Q - Quit', True, (BLACK))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/3 - title.get_height()/3))
    screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
    pg.display.update()

def draw_winner_screen():  # Fungsi untuk menampilkan menu game over
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 40)
    title = font.render('WINNER', True, (BLACK))
    restart_button = font.render('R - Restart', True, (BLACK))
    quit_button = font.render('Q - Quit', True, (BLACK))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/3 - title.get_height()/3))
    screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
    pg.display.update()

def draw_mission_status():
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 32)
    mission_text = font.render(f'Potong {mission_target} layangan musuh!', True, (BLACK))
    enemies_cut_text = font.render(f'Layangan Musuh Dipotong: {enemies_cut}/{mission_target}', True, (BLACK))
    font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 48)
    time_text = font.render(f'{time_remaining:.1f}', True, (BLACK))
    
    screen.blit(mission_text, (20, 50))
    screen.blit(enemies_cut_text, (20, 90))
    screen.blit(time_text, (SCREEN_WIDTH//2, SCREEN_HEIGHT//10))

# Class Player
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
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Player mati
        return False  # Player masih hidup

    def draw_health(self, screen):
        font = pg.font.Font(".\\assets\\fonts\\Wigglye.ttf", 32)
        color = BLACK if self.health > 30 else RED
        health_text = font.render(f'Health: {self.health}', True, color)
        screen.blit(health_text, (20, 10))

    def draw_line(self, screen):
        # Menggambar garis dari titik bawah layangan ke posisi lebih rendah
        if self.facing_left == True:
            start_pos = (self.rect.centerx + 15, self.rect.bottom - 10)
        else:
            start_pos = (self.rect.centerx - 15, self.rect.bottom - 10)
        end_pos = (SCREEN_WIDTH//2, SCREEN_HEIGHT)  # Panjang tali layangan
        pg.draw.line(screen, BLACK, start_pos, end_pos, 2)  # Tali berwarna hitam, tebal 2px

    def draw(self, screen):
        # Flip image if facing left
        image_to_draw = pg.transform.flip(self.image, True, False) if self.facing_left else self.image
        screen.blit(image_to_draw, self.rect.topleft)
        self.draw_line(screen)  # Menggambar tali layangan
        self.draw_health(screen)

# Kelas untuk layangan Musuh
class Enemy(pg.sprite.Sprite):
    def __init__(self, image):
        
        super().__init__()
        self.image = pg.transform.scale(image, (50, 50))  # Mengubah ukuran gambar
        self.rect = self.image.get_rect()
        self.rect.y = ran.randint(0, SCREEN_HEIGHT - 75)  # Posisi acak untuk y
        self.speed = ran.randint(1, 5)  # Kecepatan acak
        self.health = 50
        self.wind_speed = ran.randint(0, 5)
        self.wind_direction = ran.choice([-1, 1])

        # Tentukan arah awal: 1 untuk ke kanan, -1 untuk ke kiri
        self.direction = ran.choice([-1, 1])
        self.facing_left = self.direction == -1  # Tentukan apakah menghadap kiri

        if self.direction == 1:  # Jika bergerak ke kanan
            self.rect.x = -self.image.get_width()  # Muncul dari kiri
        else:  # Jika bergerak ke kiri
            self.rect.x = SCREEN_WIDTH  # Muncul dari kanan

    def update(self):
        if self.health > 0:
            # Gerak bebas sesuai arah (kiri atau kanan)
            self.rect.x += self.speed * self.direction
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.reset_position()
        else:
            # Jika health habis, musuh jatuh ke bawah
            self.rect.y += 5  # Gerak jatuh layangan jika health habis
            self.rect.x += self.wind_speed * self.wind_direction
            self.kill()

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            # self.kill()
            self.speed = 0  # Berhenti gerak horizontal jika nyawa habis
            return True
        return False

    def reset_position(self):
        # Mengatur ulang posisi x dan y untuk kemunculan kembali
        self.rect.y = ran.randint(0, SCREEN_HEIGHT - 75)  # Posisi y acak
        self.direction *= -1  # Ubah arah bergerak
        self.facing_left = self.direction == -1  # Perbarui arah

        # Jika bergerak ke kanan, mulai dari kiri; jika ke kiri, mulai dari kanan
        if self.direction == 1:
            self.rect.x = -self.image.get_width()  # Muncul dari kiri
        else:
            self.rect.x = SCREEN_WIDTH  # Muncul dari kanan

        self.speed = ran.randint(1, 5)  # Kecepatan acak untuk gerakan berikutnya

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):  # Periksa tabrakan
            if player.take_damage(player.damage):  # Jika pemain mati
                return True  # Tanda bahwa game over
        return False  # Masih hidup

    def check_collision_with_line(self, line_start, line_end):
        return self.rect.clipline(line_start, line_end)

    def draw_line(self, screen):
        # Menggambar garis hanya jika musuh masih memiliki health
        if self.health > 0:
            start_pos = (self.rect.centerx - 15, self.rect.bottom - 10)
            end_pos = (self.rect.centerx, SCREEN_HEIGHT)  # Panjang tali layangan
            pg.draw.line(screen, BLACK, start_pos, end_pos, 2)  # Tali berwarna hitam, tebal 2px

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Menggambar musuh ke layar
        self.draw_line(screen)  # Menggambar tali layangan jika health > 0 

def check_collisions(player, enemies):
    global enemies_cut, time_remaining
    player_line_start = (player.rect.centerx - 15, player.rect.bottom - 10) if player.facing_left else (player.rect.centerx + 15, player.rect.bottom - 10)
    player_line_end = (player.rect.centerx, player.rect.bottom + 10)

    for enemy in enemies:
        if enemy.check_collision_with_line(player_line_start, player_line_end):
            player_damage = ran.randint(1, 2)
            enemy_damage = ran.randint(1, 10)

            if player.take_damage(player_damage):
                return "player_dead"
            if enemy.take_damage(enemy_damage):
                time_remaining += 30
                enemies_cut += 1
                print("Enemy's Line Broke")
                print(f"Enemies cut: {enemies_cut}")
                break
    return "continue"

# Fungsi untuk memeriksa apakah semua musuh sudah dikalahkan
def check_all_enemies_defeated(enemies):
    for enemy in enemies:
        if enemy.health > 0:  # Masih ada musuh yang hidup
            return False
    # pg.time.wait(2000)
    return True  # Semua musuh sudah kalah

# Menambahkan beberapa musuh ke dalam kelompok enemies
enemies = pg.sprite.Group()
running = True

# Clock pygame
clock = pg.time.Clock()

while running:
    dt = clock.tick(60)

    # Menggambar semua elemen latar belakang di layar
    screen.blit(background_image, (0, 0))  # Menggambar latar belakang
    screen.blit(cloud1_sprite, (0, 0))  # Menggambar awan statis
    screen.blit(cloud2_sprite, (0, 0))  # Menggambar awan statis

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Start Menu
        if game_state == "start_menu":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_state = "kite_selection"
        
        # Kite Selection
        elif game_state == "kite_selection":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    layangan_selected = (layangan_selected - 1) % len(layangan_image)
                    select_sound.play()
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    layangan_selected = (layangan_selected + 1) % len(layangan_image)
                    select_sound.play()
                elif event.key == pg.K_SPACE:
                    player = Player(layangan_image[layangan_selected], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    game_state = "playing"
                    enemies_cut = 0
                    time_remaining = mission_time_limit
                    enemies.empty()
                    for _ in range(mission_target): 
                        enemy = Enemy(layangan_image[ran.randint(0, 3)])
                        enemies.add(enemy)

        # Game Over or Winner Screen
        elif game_state in ["game_over", "winner"]:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game_state = "kite_selection"
                elif event.key == pg.K_q:
                    running = False

    # Menggambar berdasarkan game state
    if game_state == "start_menu":
        draw_start_menu()
    elif game_state == "kite_selection":
        draw_kite_selection()
    elif game_state == "playing":
        wind_sound.play(-1)  # Pastikan suara hanya dimainkan sekali dalam game state ini

        # Kontrol untuk pemain dan pembaruan permainan
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE] or keys[pg.K_w]:
            player.jump()
        else:
            player.is_jumping = False

        player.update(mouse_pos)  # Update posisi pemain
        player.draw(screen)  # Gambar pemain
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)
        enemies.update()  # Update posisi musuh
        enemies.draw(screen)  # Gambar semua musuh

        # Cek tabrakan antara pemain dan musuh
        collision_result = check_collisions(player, enemies)
        if collision_result == "player_dead":
            game_state = "game_over"
            game_over_sound.play()
            print("Game Over! Player's health reached zero.")

        # Cek apakah semua musuh telah dikalahkan
        if check_all_enemies_defeated(enemies):
            print("All enemies defeated!")
            game_state = "winner"
            game_over_sound.play()

        draw_mission_status()

        # Hitung waktu yang tersisa untuk misi
        if time_remaining > 0:
            time_remaining -= clock.tick(60) / 100  # Kurangi waktu berdasarkan frame rate
        else:
            game_state = "game_over"
            game_over_sound.play()  # Suara game over

    elif game_state == "game_over":
        draw_game_over_screen()

    elif game_state == "winner":
        draw_winner_screen()

    pg.display.flip()  # Refresh layar

pg.quit()
