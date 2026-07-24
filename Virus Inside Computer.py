import pygame
import sys

# init
pygame.init()
display_info = pygame.display.Info()
win = pygame.display.set_mode((display_info.current_w, display_info.current_h))

# main
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill("skyblue")
        pygame.display.update()

if __name__ == "__main__":
    main()