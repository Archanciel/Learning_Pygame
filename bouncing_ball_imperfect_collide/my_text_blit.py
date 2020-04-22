import pygame as pg


class TextBox:

    def __init__(self, pos, font, bg_color, text_color=(255, 255, 255)):
        self.font = font
        self.font_height = font.get_linesize()
        self.rect = pg.Rect(pos, (200, 200))
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, screen):
        """Draw the rect and the separate text images."""
        pg.draw.rect(screen, self.bg_color, self.rect)
        lines = []
        lines.append('x: ' + str(self.rect.centerx) + ' y: ' + str(self.rect.centerx))
        lines.append('angle: ' + str(45))
        
        self.images = []  # The text surfaces.
                
        for line in lines:
        	surf = self.font.render(line, True, self.text_color)
        	self.images.append(surf)
        	
        yInit = 20

        for y, surf in enumerate(self.images):
            # Don't blit below the rect area.
            if y * self.font_height + self.font_height > self.rect.h:
                break
            screen.blit(surf, (self.rect.x, self.rect.y + yInit + y*self.font_height))

    def scale(self, rel):
        self.rect.w += rel[0]
        self.rect.h += rel[1]
        self.rect.w = max(self.rect.w, 30)  # 30 px is the minimum width.
        self.rect.h = max(self.rect.h, 30)

    def move(self, rel):
        self.rect.move_ip(rel)
        self.rect.clamp_ip(screen.get_rect())


pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
FONT = pg.font.Font(None, 22)
selected_box = None
textbox = TextBox((50, 50), FONT, (20, 50, 120))
textbox2 = TextBox((350, 100), pg.font.Font(None, 22), (20, 80, 60))

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for box in (textbox, textbox2):
                if box.rect.collidepoint(event.pos):
                    selected_box = box  # Select the colliding box.
        elif event.type == pg.MOUSEBUTTONUP:
            selected_box = None  # De-select the box.
        elif event.type == pg.MOUSEMOTION:
            if selected_box is not None:  # If a box is selected.
                if event.buttons[0]:  # Left mouse button is down.
                    selected_box.move(event.rel)
                else:
                    selected_box.scale(event.rel)

    screen.fill((30, 30, 30))
    textbox.draw(screen)
    textbox2.draw(screen)
    pg.display.flip()
    clock.tick(60) 