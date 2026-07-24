import pygame
import sys
from assets import assets

# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))
color = (135,206,235)
status = "menu"

# start
def start():
    global status

    status = "start"

def ingame():
    global status
    if status == "start":
        win10IMAGE = pygame.image.load("assets/image/logo/win10.png")
        win10IMAGE_x = 100
        win10IMAGE_y = 100
        win.blit(win10IMAGE, (win10IMAGE_x, win10IMAGE_y))

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