import pygame as pg
import random as ran

pg.init()  # Inisialisasi pygame

screen = pg.display.set_mode((800, 600))  # Konfigurasi ukuran jendela game
pg.display.set_caption("Perang Layangan")  # Konfigurasi nama jendela game

# Memanggil file gambar background
background_image = pg.image.load("Clouds5/1.png")  
moon_sprite = pg.image.load("Clouds5/2.png")  
cloud1_sprite = pg.image.load("Clouds5/4.png")  
cloud2_sprite = pg.image.load("Clouds5/5.png")  
cloud_moving_sprite = pg.image.load("Clouds5/3.png")  

# Mengubah resolusi gambar sesuai ukuran jendela game
background_image = pg.transform.scale(background_image, (800, 600))  
moon_sprite = pg.transform.scale(moon_sprite, (800, 600))  
cloud1_sprite = pg.transform.scale(cloud1_sprite, (800, 600))  
cloud2_sprite = pg.transform.scale(cloud2_sprite, (800, 600))  
cloud_moving_sprite = pg.transform.scale(cloud_moving_sprite, (800, 600))  

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
    screen.blit(title, (800 / 2 - title.get_width() / 2, 600 / 2 - title.get_height() / 2 - 20))
    screen.blit(start_button, (800 / 2 - start_button.get_width() / 2, 600 / 2 + start_button.get_height() / 2 + 20))
    pg.display.update()

def draw_game_over_screen():  # Fungsi untuk menampilkan menu game over
    screen.fill((0, 0, 0))
    font = pg.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (255, 255, 255))
    restart_button = font.render('R - Restart', True, (255, 255, 255))
    quit_button = font.render('Q - Quit', True, (255, 255, 255))
    screen.blit(title, (800/2 - title.get_width()/2, 600/2 - title.get_height()/3))
    screen.blit(restart_button, (800/2 - restart_button.get_width()/2, 600/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (800/2 - quit_button.get_width()/2, 600/2 + quit_button.get_height()/2))
    pg.display.update()

layangan_image = [
    pg.image.load("layangan1.png"),
    pg.image.load("layangan2.png"),
    pg.image.load("layangan3.png"),
    pg.image.load("layangan4.png")
]  # Memanggil file sprite layangan

layangan_selected = 0  # Layangan Default

player_image = layangan_image[layangan_selected]  # Gunakan langsung gambar yang sudah dimuat
player_image = pg.transform.scale(player_image, (50, 50))  # Ubah ukuran gambar sesuai kebutuhan

speed = 10  # Kecepatan gerakan horizontal
gravity = 0.5  # Percepatan gravitasi
jump_strength = -5  # Kekuatan lompatan
horizontal_jump_speed = 5  # Kecepatan horizontal saat melompat
vertical_velocity = 0  # Kecepatan gerakan vertikal
player_y = 400  # Posisi awal vertikal pemain

facing_left = True  # Variabel untuk menyimpan nilai apakah gambar menghadap kiri

music_volume = 0.5  # Variabel yang menampung nilai untuk volume musik
pg.mixer.music.set_volume(music_volume)  # Mengatur Volume Musik pada Game Berdasarkan Nilai yang diberikan pengguna ke variabel music_volume

running = True
player_x = 200

# Timer untuk lompatan
jump_cooldown = 3000  # Cooldown dalam milidetik (3 detik = 3000 ms)
last_jump_time = 0  # Waktu terakhir pemain melompat

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

    if cloud_moving_x > 800:  # Jika awan keluar layar, awan kembali ke awal
        cloud_moving_x = -cloud_moving_sprite.get_width()
        cloud_moving_y = ran.randint(0, 100)

    # Menampilkan gambar awan bergerak
    screen.blit(cloud_moving_sprite, (cloud_moving_x, cloud_moving_y))

    # Panggil fungsi untuk menggambar menu
    keys = pg.key.get_pressed()
    if game_state == "start_menu":
        draw_start_menu()
        if keys[pg.K_SPACE]:
            player_x, player_y = 200, 400
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
        # Gerakan kiri dan kanan menggunakan keyboard (untuk mengganti arah hadap)
        if keys[pg.K_LEFT]:
            facing_left = True  # Ganti arah hadap ke kiri
            player_x -= speed * dt / 1000  # Gerakan ke kiri
        if keys[pg.K_RIGHT]:
            facing_left = False  # Ganti arah hadap ke kanan
            player_x += speed * dt / 1000  # Gerakan ke kanan

        # Lompatan
        if keys[pg.K_SPACE]:  # Lompatan hanya saat menyentuh tanah
            vertical_velocity = jump_strength  # Lompat
            if facing_left:
                player_x -= horizontal_jump_speed  # Gerak ke kiri saat melompat
            else:
                player_x += horizontal_jump_speed  # Gerak ke kanan saat melompat

        # Mengaplikasikan gravitasi
        vertical_velocity += gravity
        player_y += vertical_velocity

        # Batas bawah layar
        if player_y >= 550:  # Jika menyentuh tanah
            player_y = 550
            vertical_velocity = 0  # Reset kecepatan vertikal saat menyentuh tanah

        # Gerakan horizontal saat jatuh berdasarkan arah hadap
        if vertical_velocity != 0:  # Saat pemain dalam keadaan jatuh
            if facing_left:
                player_x -= speed * dt / 1000  # Gerak ke kiri saat jatuh
            else:
                player_x += speed * dt / 1000  # Gerak ke kanan saat jatuh

        # Membalikkan sprite jika perlu
        if facing_left:
            player_image = pg.transform.flip(layangan_image[layangan_selected], True, False)
        else:
            player_image = layangan_image[layangan_selected]

        # Menampilkan pemain di layar
        screen.blit(player_image, (player_x, player_y))

    # Mengupdate tampilan
    pg.display.flip()

pg.quit()  # Menghentikan pygame
