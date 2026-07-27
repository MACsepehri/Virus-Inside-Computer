import pygame
import sys
import random
from assets import assets
# problem about 1920 X 1080 screen
# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))
color = (135,206,235)
status = "menu"
clock = pygame.time.Clock()
pygame.display.set_caption("Virus Inside Computer : DEMO")
FPS = 120
direction = "right"
bullet = assets.Bullet(win)
taskbar_ = pygame.image.load("assets/image/logo/taskbar.png").convert_alpha()
taskbar_ = pygame.transform.scale(
    taskbar_,
    (display_info.current_w, taskbar_.get_height())
)

folder_image = pygame.transform.scale(pygame.image.load("assets/image/logo/full-folder.png"), (100, 80))
folder_hover = pygame.transform.scale(folder_image, (110, 88))
player_middle = pygame.transform.scale(pygame.image.load("assets/image/player/middle.png"), (130, 140))
player_right = pygame.transform.scale(pygame.image.load("assets/image/player/right.png"), (130, 140))
player_left = pygame.transform.scale(pygame.image.load("assets/image/player/left.png"), (130, 140))
player = player_middle
playerX = 10
if display_info.current_h > 768:
    playerY = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
else:
    playerY = display_info.current_h - (taskbar_.get_height() + (taskbar_.get_height() / 2)) - player.get_height() + 20
jump = False
if display_info.current_h > 768:
    come_down_y = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
else:
    come_down_y = display_info.current_h - (taskbar_.get_height() + (taskbar_.get_height() / 2)) - player.get_height() + 20
jump_velocity = 0
on_platform = False
platform_y = None

# phase massage info show
phase_1_messageinfo_show = True
phase_1_timer = 0

# draw folders
draw_folder = False

# phase 1 data
detected_viruses = 0
detected_glitches = 0
detect_times = 10
detect_timer = 0
detect_message_show = False
show_it_again_phase_1 = True
glitch_image_list, is_virus_in_glitch = assets.add_glitch()

# player data
player_heart = 100
antivirus_defender = assets.Button(win, display_info.current_w - 300, 70, 64, 64, assets.small_font, "", image=pygame.transform.scale(pygame.image.load("assets/image/player_tools/antivirus-defender.png"), (64, 64)), button_color=(174, 215, 232), hover_color=(160, 213, 235), r=5)
antivirus_attacker = assets.Button(win, display_info.current_w - 230, 70, 64, 64, assets.small_font, "", image=pygame.transform.scale(pygame.image.load("assets/image/player_tools/antivirus-attacker.png"), (64, 64)), button_color=(174, 215, 232), hover_color=(160, 213, 235), r=5)
click_cooldown = 0
phase_entry_cooldown = 0
player_collision_cooldown = 0
player_collision_entry = 0
hover = False

# attack and defend button hover
attack_button_hover = False
defend_button_hover = False

# generate viruses
def generate_virus():
    l = []
    img1 = pygame.image.load("assets/image/enemy/easy.png")
    img2 = pygame.image.load("assets/image/enemy/mediume.png")
    for i in range(random.randint(7, 16)):
        img = random.choice([img1, img2])
        x = random.randint(int(display_info.current_w / 2), display_info.current_w - int(img.get_width() / 2))
        if display_info.current_h > 768:
            y = display_info.current_h - (taskbar_.get_height() * 2)
        else:
            y = display_info.current_h - (taskbar_.get_height() + (taskbar_.get_height() / 2)) - 100

        l.append((pygame.transform.scale(img, (100, 100)), (x, y)))

    return l

def draw_enemy_phase_1(generated_enmeis):
    for enemy in generated_enmeis:
        img = enemy[0]
        pos = enemy[1]
        win.blit(img, pos)

def collision(rect1, rect2):
    return rect1.colliderect(rect2)

e = generate_virus()
# phone
def detect():
    global detected_glitches, detected_glitches, detect_times, detect_timer, detect_message_show, show_it_again_phase_1
    if show_it_again_phase_1:
        if (detect_times - 1) <= 0:
            detect_message_show = True
            show_it_again_phase_1 = False

def phone():
    global status, detect_message_show, detect_timer, detect_message_show, detect_times, hover

    if status == "phase_1":
        assets.draw_text(f"Detected virus: {detected_viruses}\nDetected glitch (might be virus): {detected_glitches}", assets.font, "black", win, 20, 20)
        btn = [ assets.Button(win, 20, 150, 200, 90, assets.font, f"Detect ({detect_times})") ]
        assets.draw_button(btn)
        hover = btn[0].hover
        assets.button_action(btn, [ detect ])

    if detect_message_show:
        if int(detect_timer) <= 100:
            assets.draw_text("Not enough detecting data", assets.font, "black", win, 500, 300)
            detect_times = 0
            detect_timer += 0.1
        else:
            detect_message_show = False

# phases
def videos():
    global status, playerX, playerY, phase_entry_cooldown


    status = "phase_1"
    playerX = 10
    if display_info.current_h > 768:
        playerY = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
    else:
        playerY = display_info.current_h - (taskbar_.get_height() + (taskbar_.get_height() / 2)) - player.get_height() + 20
        phase_entry_cooldown = 30
    phase_1()

if display_info.current_h > 768:
    folder_list = [
        (100, 100, 100, 80, ["Game", 100, 180, lambda: ...]),
        (400, 200, 100, 80, ["Photos", 400, 280, lambda: ...]),
        (200, 400, 100, 80, ["Docs", 200, 480, lambda: ...]),
        (display_info.current_w - 300, 500, 100, 80, ["Videos", display_info.current_w - 300, 580, videos])
    ]
else:
    folder_list = [
        (100, 70, 100, 80, ["Game", 100, 150, lambda: ...]),
        (400, 170, 100, 80, ["Photos", 400, 250, lambda: ...]),
        (200, 340, 100, 80, ["Docs", 200, 420, lambda: ...]),
        (display_info.current_w - 300, 430, 100, 80, ["Videos", display_info.current_w - 300, 510, videos])
    ]

# player movement
def draw_player():
    global playerX, playerY, jump, come_down_y, jump_velocity, player, on_platform, platform_y, draw_folder, direction

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        playerX -= 3
        player = player_left
        direction = "left"
    elif keys[pygame.K_d]:
        playerX += 3
        player = player_right
        direction = "right"
    else:
        player = player_middle

    if keys[pygame.K_SPACE] and not jump:
        jump = True
        jump_velocity = -20
        on_platform = False
        platform_y = None

    if jump:
        if keys[pygame.K_SPACE]:
            jump_velocity += 0.5
        else:
            jump_velocity += 1.5
            
        playerY += jump_velocity

        if draw_folder:
            if jump_velocity > 0:
                for folder in folder_list:
                    folder_rect = pygame.Rect(folder[0], folder[1], folder[2], folder[3])
                    player_rect = pygame.Rect(playerX, playerY + player.get_height() - 10, 
                                            player.get_width(), 10)
                    
                    if player_rect.colliderect(folder_rect):
                        playerY = folder[1] - player.get_height()
                        jump = False
                        jump_velocity = 0
                        on_platform = True
                        platform_y = folder[1]
                        break
            
        if playerY >= come_down_y:
            playerY = come_down_y
            jump = False
            jump_velocity = 0
            on_platform = False
            platform_y = None

    if draw_folder:
        if not jump:
            on_platform = False
            platform_y = None

            for folder in folder_list:
                horizontal = (
                    playerX + player.get_width() > folder[0]
                    and playerX < folder[0] + folder[2]
                )
                standing = abs((playerY + player.get_height()) - folder[1]) <= 3

                if horizontal and standing:
                    on_platform = True
                    platform_y = folder[1]

                    button = [
                        assets.Button(win, folder[0] - 50, folder[1] - 60, 200, 50, assets.font, "Enter")]
                    assets.draw_button(button)
                    assets.button_action(button, [ folder[4][3] ])
                    break

        if not on_platform and playerY < come_down_y:
            if status == "phase_1":
                playerY += 1.5
            else:
                playerY += 0.5
        
        if not on_platform and playerY < come_down_y:
            if status == "phase_1":
                playerY += 1.5
            else:
                playerY += 0.5
            if draw_folder:
                player_rect = pygame.Rect(playerX, playerY + player.get_height() - 5, 
                                        player.get_width(), 5)
                for folder in folder_list:
                    folder_rect = pygame.Rect(folder[0], folder[1], folder[2], folder[3])
                    if player_rect.colliderect(folder_rect):
                        if playerY + player.get_height() <= folder[1] + 10:
                            playerY = folder[1] - player.get_height()
                            on_platform = True
                            platform_y = folder[1]
                            break
            
            if playerY >= come_down_y:
                playerY = come_down_y
                on_platform = False
                platform_y = None

    if playerX <= 0:
        playerX = 0
    elif playerX >= display_info.current_w - player.get_width():
        playerX = display_info.current_w - player.get_width()
    
    win.blit(player, (playerX, playerY))

# message box
def phase1_messagebox_info():
    global phase_1_messageinfo_show, phase_1_timer
    if phase_1_messageinfo_show:
        assets.draw_text("Remove viruses, fight with them and go to next level.", assets.font, "black", win, 100, 100)
        if int(phase_1_timer) <= 100:
            phase_1_timer += 0.05
        else:
            phase_1_messageinfo_show = False

# draw taskbar
def taskbar():
    if display_info.current_h > 768:
        win.blit(taskbar_, (0, display_info.current_h - taskbar_.get_height()))
    else:
        win.blit(taskbar_, (0, display_info.current_h - (taskbar_.get_height() + (taskbar_.get_height() / 2))))

# start
def start():
    global status

    status = "start"

def ingame():
    global status, folder_list, draw_folder
    if status == "start":
        win10IMAGE = pygame.image.load("assets/image/logo/win10.png")
        win10_rect = win10IMAGE.get_rect()
        win10_rect.center = win.get_rect().center
        win.blit(win10IMAGE, win10_rect)

        mouse = pygame.mouse.get_pos()

        for folder in folder_list:
            x, y, w, h = folder[:4]
            hover_rect = pygame.Rect(x - 5, y - 4, 110, 88)
            if hover_rect.collidepoint(mouse):
                win.blit(folder_hover, (x - 5, y - 4))
            else:
                win.blit(folder_image, (x, y))
        taskbar()
        draw_player()
        draw_folder = True
        for folder in folder_list:
            assets.draw_text(folder[4][0], assets.font, "black", win, folder[4][1], folder[4][2])

def player_on_folder(folder):
    horizontal = (
        playerX + player.get_width() > folder[0]
        and playerX < folder[0] + folder[2]
    )

    standing = abs((playerY + player.get_height()) - folder[1]) <= 3

    return horizontal and standing

# phase parts
def phase_1():
    global status, draw_folder, phase_1_messageinfo_show
    global click_cooldown, phase_entry_cooldown
    global player_collision_cooldown, player_heart, hover
    global attack_button_hover, defend_button_hover, antivirus_attacker, antivirus_defender

    if status != "phase_1":
        return

    if phase_entry_cooldown > 0:
        phase_entry_cooldown -= 1

    if click_cooldown > 0:
        click_cooldown -= 1
    elif phase_entry_cooldown <= 0:
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            if attack_button_hover:
                bullet.add_new_bullet(
                    playerX + player.get_width() // 2,
                    playerY + player.get_height() // 2,
                    direction
                )
                click_cooldown = 10

            elif defend_button_hover:
                click_cooldown = 10

            elif not hover:
                bullet.add_new_bullet(
                    playerX + player.get_width() // 2,
                    playerY + player.get_height() // 2,
                    direction
                )
                click_cooldown = 10

    if player_collision_cooldown > 0:
        player_collision_cooldown -= 1
    else:
        player_rect = player.get_rect(topleft=(playerX, playerY))

        for virus_img, virus_pos in e:
            virus_rect = virus_img.get_rect(topleft=virus_pos)

            if player_rect.colliderect(virus_rect):
                player_heart = max(0, player_heart - 1)
                player_collision_cooldown = 10
                break

    speed = 1.5
    for i in range(len(e)):
        virus_img, (x, y) = e[i]
        enemy_x = x + virus_img.get_width() / 2
        enemy_y = y + virus_img.get_height() / 2

        player_center_x = playerX + player.get_width() / 2
        player_center_y = playerY + player.get_height() / 2

        dx = player_center_x - enemy_x
        dy = player_center_y - enemy_y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance

        x += dx * speed
        y += dy * speed

        e[i] = (virus_img, (x, y))

    taskbar()
    draw_player()
    draw_folder = False
    draw_enemy_phase_1(e)

    phase1_messagebox_info()

    assets.draw_button([antivirus_defender, antivirus_attacker])

    if antivirus_attacker.hover:
        attack_button_hover = True
    else:
        attack_button_hover = False

    if antivirus_defender.hover:
        defend_button_hover = True
    else:
        defend_button_hover = False

    filled_width = max(0, (player_heart / 100) * 200)

    pygame.draw.rect(win, (80, 80, 80), (display_info.current_w - 300, 20, 200, 40))
    pygame.draw.rect(win, (255, 60, 60), (display_info.current_w - 300, 20, filled_width, 40))

    pygame.draw.rect(win, (120, 0, 0), (display_info.current_w - 300, 20, 200, 40), 3)
    assets.draw_text(f"Health: {player_heart}", assets.small_font, "black", win, display_info.current_w - 290, 27)
    assets.draw_text("Attack: LMB\nDefend: RMB", assets.small_font, "black", win, display_info.current_w - 150, 70)

    assets.draw_text(f"FPS: {clock.get_fps():.0f}", assets.small_font, "black", win, display_info.current_w - 90, 27)

    if not phase_1_messageinfo_show:
        phone()

def spawn_enemy():
    global display_info

    img1 = pygame.image.load("assets/image/enemy/easy.png").convert_alpha()
    img2 = pygame.image.load("assets/image/enemy/mediume.png").convert_alpha()

    img = random.choice([img1, img2])

    x = random.randint(display_info.current_w // 2, display_info.current_w - 100)

    if display_info.current_h > 768:
        y = display_info.current_h - (taskbar_.get_height() * 2)
    else:
        y = display_info.current_h - (
            taskbar_.get_height() + taskbar_.get_height() / 2
        ) - 100

    img = pygame.transform.scale(img, (100, 100))
    return (img, (x, y))

# update
def update():
    global status

    if status == "menu":
        btn = [
            assets.Button(win, 0, 250, 200, 90, assets.font, "Start", middle=True),
            assets.Button(win, 0, 350, 200, 90, assets.font, "Setting", middle=True),
            assets.Button(win, 0, 450, 200, 90, assets.font, "Exit", middle=True)
        ]
        assets.draw_button(btn)
        assets.button_action(btn, [start, lambda: ..., sys.exit])

    ingame()
    phase_1()

# main
def main():
    global mouse_pos, status

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for folder in folder_list:
                        hover_rect = pygame.Rect(folder[0] - 5, folder[1] - 4, 110, 88)
                        if hover_rect.collidepoint(event.pos):
                            folder[4][3]()

        win.fill(color)
        update()
        if not defend_button_hover:
            bullet.move()
            bullet.check_collision(e)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
