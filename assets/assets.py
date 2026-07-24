import pygame

pygame.init()

font = pygame.font.Font("assets/font/font.ttf", 48)
small_font = pygame.font.Font("assets/font/font.ttf", 32)

class Button:
    def __init__(self, win, x, y, width, height, font=None, text="", middle=False, text_color="white", button_color="black", hover_color=(21,21,21), image=None, r=5, win_object=None):
        self.win_object = win_object if win_object is not None else win
        
        if middle and self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            x = (screen_width - width) // 2
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        try:
            if font is not None: 
                self.font = font
            else: 
                self.font = pygame.font.Font(None, 32)
        except:
            self.font = pygame.font.Font(None, 32)
            
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.clicked = False
        self.visible = True
        self.middle = middle
        self.image = image if image != "" else None
        self.border_radius = r

    def draw(self):
        if not self.visible:
            return
        
        if self.middle and self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            self.rect.x = (screen_width - self.width) // 2
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.win_object, self.hover_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.win_object, self.button_color, self.rect, border_radius=self.border_radius)

        if self.image is not None:
            text_surface = self.image
        else:
            text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.win_object.blit(text_surface, text_rect)

    def is_clicked(self):
        if not self.visible:
            return False
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_x, mouse_y) and mouse_click:
            if not self.clicked:
                self.clicked = True
                return True
        else:
            self.clicked = False
        return False
    
    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
        
    def set_middle(self):
        if self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            self.rect.x = (screen_width - self.width) // 2

def draw_text(text, font, color, win, x, y):
    win.blit(font.render(text, True, color), (x, y))

def draw_button(btn_list, action_list):
    i = 0
    for btn in btn_list:
        if btn.is_clicked():
            action_list[i]()
        i += 1