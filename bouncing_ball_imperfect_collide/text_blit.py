import pygame as pg


class TextBox:

    def __init__(self, text, pos, font, bg_color, text_color=(255, 255, 255)):
        self.font = font
        self.font_height = font.get_linesize()
        self.text = text.split()  # Single words.
        self.rect = pg.Rect(pos, (200, 200))
        self.bg_color = bg_color
        self.text_color = text_color
        self.render_text_surfaces()

    def render_text_surfaces(self):
        """Create a new text images list when the rect gets scaled."""
        self.images = []  # The text surfaces.
        line_width = 0
        line = []
        space_width = self.font.size(' ')[0]

        # Put the words one after the other into a list if they still
        # fit on the same line, otherwise render the line and append
        # the resulting surface to the self.images list.
        for word in self.text:
            line_width += self.font.size(word)[0] + space_width
            # Render a line if the line width is greater than the rect width.
            if line_width > self.rect.w:
                surf = self.font.render(' '.join(line), True, self.text_color)
                self.images.append(surf)
                line = []
                line_width = self.font.size(word)[0] + space_width

            line.append(word)

        # Need to render the last line as well.
        surf = self.font.render(' '.join(line), True, self.text_color)
        self.images.append(surf)

    def draw(self, screen):
        """Draw the rect and the separate text images."""
        pg.draw.rect(screen, self.bg_color, self.rect)

        for y, surf in enumerate(self.images):
            # Don't blit below the rect area.
            if y * self.font_height + self.font_height > self.rect.h:
                break
            screen.blit(surf, (self.rect.x, self.rect.y+y*self.font_height))

    def scale(self, rel):
        self.rect.w += rel[0]
        self.rect.h += rel[1]
        self.rect.w = max(self.rect.w, 30)  # 30 px is the minimum width.
        self.rect.h = max(self.rect.h, 30)
        self.render_text_surfaces()

    def move(self, rel):
        self.rect.move_ip(rel)
        self.rect.clamp_ip(screen.get_rect())


text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum."""
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
FONT = pg.font.Font(None, 34)
selected_box = None
textbox = TextBox(text, (50, 50), FONT, (20, 50, 120))
textbox2 = TextBox(text, (350, 100), pg.font.Font(None, 22), (20, 80, 60))

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