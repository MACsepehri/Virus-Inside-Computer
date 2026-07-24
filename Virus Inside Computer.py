import pygame
import sys
from assets import assets

# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))
color = (135,206,235)
status = "menu"

folder_list = [
    (100, 100),
    (400, 200),
    (200, 400),
    (display_info.current_w - 300, 500)
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

# player movement
def draw_player():
    global playerX

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerX -= 3
    elif keys[pygame.K_d]:
        playerX += 3

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
            win.blit(folder_image, pos)
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