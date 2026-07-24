import pygame
import sys
from assets import assets

# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))
color = (135,206,235)
status = "menu"

# phases
def videos():
    global status
    global playerX, playerY

    status = "phase_1"
    playerX = 10
    playerY = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
    phase_1()

folder_list = [
    (100, 100, 100, 80, ["Game", 100, 180, lambda: ...]),
    (400, 200, 100, 80, ["Photos", 400, 280, lambda: ...]),
    (200, 400, 100, 80, ["Docs", 200, 480, lambda: ...]),
    (display_info.current_w - 300, 500, 100, 80, ["Videos", display_info.current_w - 300, 580, videos])
]

taskbar_ = pygame.image.load("assets/image/logo/taskbar.png").convert_alpha()
taskbar_ = pygame.transform.scale(
    taskbar_,
    (display_info.current_w, taskbar_.get_height())
)

folder_image = pygame.transform.scale(pygame.image.load("assets/image/logo/full-folder.png"), (100, 80))
player_middle = pygame.transform.scale(pygame.image.load("assets/image/player/middle.png"), (130, 140))
player_right = pygame.transform.scale(pygame.image.load("assets/image/player/right.png"), (130, 140))
player_left = pygame.transform.scale(pygame.image.load("assets/image/player/left.png"), (130, 140))
player = player_middle
playerX = 10
playerY = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
jump = False
come_down_y = display_info.current_h - taskbar_.get_height() - player.get_height() + 20
jump_velocity = 0
on_platform = False
platform_y = None

# player movement
def draw_player():
    global playerX, playerY, jump, come_down_y, jump_velocity, player, on_platform, platform_y

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        playerX -= 3
        player = player_left
    elif keys[pygame.K_d]:
        playerX += 3
        player = player_right
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
                    assets.Button(
                        win,
                        folder[0] - 50,
                        folder[1] - 60,
                        200,
                        50,
                        assets.font,
                        "Enter"
                    )
                ]
                assets.draw_button(button)
                assets.button_action(button, [ folder[4][3] ])
                break

        if not on_platform and playerY < come_down_y:
            playerY += 1.5
        
        if not on_platform and playerY < come_down_y:
            playerY += 1.5
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

# draw taskbar
def taskbar():
    win.blit(taskbar_, (0, display_info.current_h - taskbar_.get_height()))

# start
def start():
    global status

    status = "start"

def ingame():
    global status, folder_list
    if status == "start":
        win10IMAGE = pygame.image.load("assets/image/logo/win10.png")
        win10_rect = win10IMAGE.get_rect()
        win10_rect.center = win.get_rect().center
        win.blit(win10IMAGE, win10_rect)

        for pos in folder_list:
            win.blit(folder_image, (pos[0], pos[1]))
        taskbar()
        draw_player()
        for folder in folder_list:
            assets.draw_text(folder[4][0], assets.font, "black", win, folder[4][1], folder[4][2])

# phase parts
def phase_1():
    global status

    if status == "phase_1":
        taskbar()
        draw_player()

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill(color)
        update()
        pygame.display.update()

if __name__ == "__main__":
    main()