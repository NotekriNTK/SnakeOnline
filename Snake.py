import pygame
from pygame.locals import QUIT, K_w, K_s, K_a, K_d, K_q,K_DOWN,K_UP,K_LEFT,K_RIGHT, KEYDOWN, K_SPACE
import Entities
import regex as re
from random import randint

input_movement = {K_w:'y-',K_s:'y+',K_d:'x+',K_a:'x-'}
last_movement = 'x+'

pygame.init()

#   Global  Static  Variables
TILE_SIZE:int   = 40
WIDTH:int       = 17
HEIGHT:int      = 17

SCREEN_HEIGHT = HEIGHT*TILE_SIZE
SCREEN_WIDTH = HEIGHT*TILE_SIZE
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

snake_colours = [
        (165, 38, 176),     #   Purple
        (240, 155, 89)      #   Brown
]
bg_colours = [(119, 221, 119),(106, 196, 106)]

clock = pygame.time.Clock()

player = Entities.Player(5,5,snake_colours[0])

players = {"P1":{"lastmovement":"-x","newmovement":"-x","player":Entities.Player(5,5,snake_colours[0])},
           "P2":{"lastmovement":"-x","newmovement":"-x","player":Entities.Player(5,10,snake_colours[1])}}
#player1 = Entities.Player(8,6,snake_colours[1])

tick = 0
new_movement = "x-"
apple = Entities.Apple(10,10)
pygame.display.set_caption("Snake MP")
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
            if event.key in input_movement.keys():
                new_movement = input_movement[event.key]
                if not re.sub('[-+]','',last_movement) in new_movement:
                    #send new movement to server...
                    pass
                else:
                    new_movement = last_movement
            if event.key == K_SPACE:
                apple.new_position()
    
    try:
        pygame.display.update()
    except:
        print('Shutting down application...')
        break

    game_screen.fill(bg_colours[0])

    _ = 0
    for y in range(0,17):
        for x in range(0,17):
            if _ % 2 == 0:
                pygame.draw.rect(game_screen, bg_colours[1], pygame.Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
            _ += 1
    
    #   Draw snakes
    for body in Entities.all_bodies:
        body.render(game_screen, pygame)

    #   Draw apple
    apple.render(game_screen, pygame)

    if tick > 6:
        tick = 0
        last_movement = new_movement
        player.direction = new_movement
        player.update()
        if apple == player.head:
            player.eat()
            apple.new_position()
            

    tick += 1
    pygame.display.flip()
    clock.tick(60)