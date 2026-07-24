import pygame
import sys
from assets import assets

# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))
status = "menu"

# start
def start():
    pass

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

# main
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill("skyblue")
        update()
        pygame.display.update()

if __name__ == "__main__":
    main()