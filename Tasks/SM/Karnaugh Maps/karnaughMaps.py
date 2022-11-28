import ctypes
import sys

bits = 4
try:
    import pygame
except:
    print("Pygame module not installed, use pip install pygame")

if bits == 2:
    letters = ["A", "B"]
    grayCode = ["0","1"]
elif bits == 4:
    letters = ["AB", "CD"]
    grayCode = ["00", "01", "11", "10"]
else:
    print("Number of bits is not supported, use only 2 or 4")

class UIObject(object):
    def __init__(self, rect = [1,1,1,1], active = True, default_colour = ((0,0,0)), hovered_colour = (pygame.Color('slategray'))):
        pass
  
class Button: #to make button generation, reactivity and rendering easier
    '''Class to make buttons'''
    def __init__(self, rect= [1, 1, 1, 1], active= True, default_colour= ((0, 0, 0)), hovered_colour= (pygame.Color('slategray')), fill= -1, middle= None, text= None, font= None, fontSize= 32, textColour= (0, 0, 0)):
        self.fill = fill
        self.rect = pygame.Rect(rect)         #sets the values for the button
        self.default_colour = default_colour  
        self.hovered_colour = hovered_colour
        self.active = active
        self.selected = False
        self.text = text
        if text != None:   #if the button has text
            self.font = pygame.font.Font(font, fontSize)
            self.textRender = self.font.render(text, False, textColour)
            self.rect.width = self.textRender.get_width() + 10 #makes the button automatically adjust to the size of the text
            self.rect.height = fontSize + 10
        if middle != None:
            self.rect.midtop = middle  #for setting an optional middle coordinate, easier for alignment
        self.alpha = 255   #for transparency
        
    def draw(self, surface, mouse_coords):   #rendering
        '''Renders button and associated text'''
        if self.active == False:   #if button is inactive, cannot be reacted with or clicked
            pygame.draw.rect(surface, self.default_colour, self.rect, self.fill)
        elif self.selected == True: #for multiselectionbutton, where button stays pressed down
            pygame.draw.rect(surface, self.hovered_colour, self.rect, 0)
        elif self.hover(mouse_coords): #if hovered over, buttons react and turn grey
            pygame.draw.rect(surface, self.hovered_colour, self.rect, 0)
        else:
            pygame.draw.rect(surface, self.default_colour, self.rect, self.fill) #normal colour button
            
        if self.text != None: 
            self.textRender.set_alpha(self.alpha) #sets transparency, needed for when in game and menu inactive
            topText = (self.rect.height - self.textRender.get_height()) // 2  #alignment
            leftText = (self.rect.width - self.textRender.get_width()) // 2
            surface.blit(self.textRender, (self.rect.x + leftText, self.rect.y + topText))
            
    def hover(self, mouse_coords):
        '''Checks if button is being hovered over'''
        if self.active == False: 
            return False
        mouse_rect = pygame.Rect(mouse_coords, [1, 1])
        return mouse_rect.colliderect(self.rect)

class TextBox:
    '''Class for making simple textboxes'''
    def __init__(self, rect, text, fontSize, font= None, active= True, default_colour= ((0, 0, 0)), text_colour= ((0, 0, 0)), middle= None, left= None, right= None):
        self.rect = pygame.rect.Rect(rect)  #initialises attributes
        self.active = active
        self.colour = default_colour
        self.text_colour = text_colour
        self.text = text
        self.font = pygame.font.Font(font, fontSize)
        self.textRender = self.font.render(self.text, False, self.text_colour)
        self.rect.width = self.textRender.get_width() + 10 #adjusts to size of text
        self.rect.height = fontSize + 10
        if middle != None:            #ability to anchor textbox along a certain edge
            self.rect.midtop = middle
        if left != None:
            self.rect.x = left
        if right != None:
            self.rect.x = right - self.rect.width
        self.alpha = 255    
                
    def draw(self, surface):
        '''Renders textbox'''
        if self.active:
            self.textRender.set_alpha(self.alpha)
            surface.blit(self.textRender, (self.rect.x + 5, self.rect.y + 5))

class KarnaughMap:
    def __init__(self, surface, offset):
        self.headers =  None
    
def main():
    user32 = ctypes.windll.user32 
    screensize = user32.GetSystemMetrics(1)
    screensize /= 1.5
    surface = pygame.display.set_mode((screensize, screensize))
    rect = pygame.rect.Rect(0,0,10,10)
    surface.fill(pygame.Color("white"))
    pygame.display.flip()
    while True:
        pygame.draw.rect(surface, pygame.Color("white"), rect, 0)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()