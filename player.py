import pygame

class Player():
    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        ''' Dibuja al jugador '''
        pygame.draw.rect(win, self.color, self.rect)
    
    def move(self):
        ''' Movimiento del jugador al hacer click a una tecla en especifico '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        
        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel
        
        if keys[pygame.K_q]:
            self.run = False 

        self.update()

    def update(self): 
        ''' Actualiza la posicion del jugador '''
        self.rect = (self.x, self.y, self.width, self.height)
