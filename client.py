from __future__ import annotations
from typing import Any
import pygame
from pygame import mixer
from network import Network
from player import Player
from pymunk import Body, Space, Circle, Poly
from pymunk.pygame_util import DrawOptions
import yaml


class HeadSoccer:
    
    BALL_RADIUS:int = 20
    WIDTH = 1000
    HEIGHT = 600
    GRAVITY_X:int = 0
    GRAVITY_Y:int = 981
    FPS:int = 60
    config: Any
    path: str
    

    def __init__(self):
        with open('config.yml', 'r') as f:
            self.config = yaml.safe_load(f)
            self.path = self.config['path']

        self.window = pygame.display.set_mode((HeadSoccer.WIDTH, HeadSoccer.HEIGHT))
        pygame.display.set_caption("HeadSoccer")
        self.space = Space()
        self.space.gravity = (HeadSoccer.GRAVITY_X, HeadSoccer.GRAVITY_Y)
        self.draw_options:DrawOptions = DrawOptions(self.window)
        
        self.ball = self.create_ball(self.space, HeadSoccer.BALL_RADIUS, 10)
        self.image = pygame.image.load(self.path + "football.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, ((HeadSoccer.BALL_RADIUS + 2) * 3, (HeadSoccer.BALL_RADIUS + 2) * 3)).convert_alpha()
        
        self.bg_img = pygame.image.load(self.path + 'Fondo.jpg').convert_alpha()
        self.bg_img = pygame.transform.scale(self.bg_img, (1000, 600)).convert_alpha()

        self.create_boundaries(self.space, HeadSoccer.WIDTH, HeadSoccer.HEIGHT)
    
    def create_boundaries(self, space, width, height) -> None:
        ''' Crea los bordes de la pantalla '''
        rects = [
            [(width / 2, height - 10), (width, 20)],
            [(width / 2, 10), (width, 20)],
            [(10, height / 2), (20, height)],
            [(width - 10, height / 2), (20, height)],
        ]

        for pos, size in rects:
            body = Body(body_type=Body.STATIC)
            body.position = pos
            shape = Poly.create_box(body, size)
            shape.elasticity = 0.9
            shape.friction = 0.5
            space.add(body, shape)

    def create_ball(self, space, radius, mass) -> Circle:
        ''' Crea la pelota y retorna la forma '''
        body = Body()
        body.position = (300, 300)
        shape = Circle(body, radius*1.5)
        shape.mass = mass
        shape.elasticity = 0.9
        shape.friction = 0.4
        shape.color = (255, 0, 0, 100)
        space.add(body, shape)
        return shape

    def redrawWindow(self, player:Player, player2:Player) -> None:
        ''' Dibuja todos los componentes y actualiza la pantalla'''
        self.window.blit(self.bg_img, (0,0))
        self.space.debug_draw(self.draw_options)
        #pygame.draw.line(window, (0, 0, 0), (0, 500), (1000, 500), 5)
        player.draw(self.window)
        player2.draw(self.window)
        if self.ball:
            pos_x, pos_y = self.ball.body.position
            self.window.blit(self.image, (pos_x - (HeadSoccer.BALL_RADIUS + 2)*1.5, pos_y - (HeadSoccer.BALL_RADIUS + 2)*1.5))
        pygame.display.update()
    
    def _reproducir_musica(self) -> None:
        ''' Abre el archivo mp3 y lo reproduce '''
        mixer.init()
        mixer.music.load(self.path + "champions.mp3")
        mixer.music.set_volume(0.5)
        mixer.music.play()
    
    def main(self) -> None:
        ''' Ejecuta el juego '''
        print("Empezando...")
        network = Network()
        run = True
        player = network.getP()
        clock = pygame.time.Clock()
        self._reproducir_musica()
        while run:
            player2 = network.send(player) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            player.move()
            self.redrawWindow(player, player2)
            self.space.step(1 / HeadSoccer.FPS)
            clock.tick(HeadSoccer.FPS)


if __name__ == '__main__':
    game = HeadSoccer()
    game.main()