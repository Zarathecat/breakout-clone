# Copyright 2016 Zara Zaimeche

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygame, random, sys
from pygame.locals import *

main_clock = pygame.time.Clock()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
PLAYERMOVESPEED = 15
BALLMOVESPEED = 5

lives = 4

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 175, 0)

pygame.init()

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
pygame.mouse.set_visible(False)

def end_game():

    pygame.quit()
    sys.exit()

player = {"rect":pygame.Rect(0, WINDOWHEIGHT-20, 80, 20), "colour":GREEN}

ball = {"rect":pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 5,5), "colour":MAGENTA}

bricks = []

for i in range(15):
    brick_1 = {"rect":pygame.Rect(i*40, 0, 39, 10), "colour":RED}
    brick_2 = {"rect":pygame.Rect(i*40+10, 20, 39, 10), "colour":ORANGE}
    brick_3 = {"rect":pygame.Rect(i*40, 40, 39, 10), "colour":YELLOW}
    brick_4 = {"rect":pygame.Rect(i*40+10, 60, 39, 10), "colour":GREEN}
    brick_5 = {"rect":pygame.Rect(i*40, 80, 39, 10), "colour":CYAN}
    brick_6 = {"rect":pygame.Rect(i*40+10, 100, 39, 10), "colour":BLUE}
    brick_7 = {"rect":pygame.Rect(i*40, 120, 39, 10), "colour":WHITE}


    bricks.append(brick_1)
    bricks.append(brick_2)
    bricks.append(brick_3)
    bricks.append(brick_4)
    bricks.append(brick_5)
    bricks.append(brick_6)
    bricks.append(brick_7)


move_player_right = move_player_left = False

ball_up_right = ball_up_left = ball_down_right = ball_down_left = False

ball_down_left = True #arbitrarily selected start dir

while True:
    window_surface.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            end_game()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
               end_game()
            if event.key == K_SPACE:
               PLAYERMOVESPEED = PLAYERMOVESPEED * 2

            if event.key == K_LEFT:
                move_player_right = False
                move_player_left = True

            if event.key == K_RIGHT:
                move_player_left = False
                move_player_right = True

        if event.type == KEYUP:
            if event.key == K_SPACE:
               PLAYERMOVESPEED = PLAYERMOVESPEED /2

            if event.key == K_LEFT:
                move_player_left = False
            if event.key == K_RIGHT:
                move_player_right = False

    if move_player_left:
        if player["rect"].left > 0:
            player["rect"].left -= PLAYERMOVESPEED
    if move_player_right:
        if player["rect"].right < WINDOWWIDTH:
            player["rect"].right += PLAYERMOVESPEED

    if ball_up_right:

        for brick in bricks[:]:
            if brick["rect"].colliderect(ball["rect"]):
                bricks.remove(brick)
                ball_up_right = False
                ball_down_right = True

    if ball_up_right: #as two ifs so the status doesn't change mid-execution

        if ball["rect"].top > 0:
            if ball["rect"].right < WINDOWWIDTH:
                ball["rect"].top -= BALLMOVESPEED
                ball["rect"].right += BALLMOVESPEED
            else:
                ball_up_right = False
                ball_up_left = True
        else:
            ball_up_right = False
            ball_down_right = True 
 
    if ball_up_left:

        for brick in bricks[:]:
            if brick["rect"].colliderect(ball["rect"]):
                bricks.remove(brick)
                ball_up_left = False
                ball_down_left = True

    if ball_up_left: #and again

        if ball["rect"].top > 0:
            if ball["rect"].left > 0:
                ball["rect"].top -= BALLMOVESPEED
                ball["rect"].left -= BALLMOVESPEED
            else:
                ball_up_left = False
                ball_up_right = True
        else:
            ball_up_left = False
            ball_down_left = True


    if ball_down_right:

        for brick in bricks[:]:
            if brick["rect"].colliderect(ball["rect"]):
                bricks.remove(brick)
                ball_down_right = False
                ball_up_right = True

    if ball_down_right: #you get the picture


        if ball["rect"].colliderect(player["rect"]):
            if ball["rect"].centerx < player["rect"].centerx:
                ball_down_right = False
                ball_up_left = True
            if ball["rect"].centerx > player["rect"].centerx:
                ball_down_right = False
                ball_up_right = True

    if ball_down_right: #you get the picture

        if ball["rect"].bottom < WINDOWHEIGHT:
            if ball["rect"].right < WINDOWWIDTH:
                ball["rect"].bottom += BALLMOVESPEED
                ball["rect"].right += BALLMOVESPEED
            else:
                ball_down_right = False
                ball_down_left = True
        else:
            ball_down_right = False
            ball_up_right = True


    if ball_down_left:

        for brick in bricks[:]:
            if brick["rect"].colliderect(ball["rect"]):
                bricks.remove(brick)
                ball_down_left = False
                ball_up_left = True

    if ball_down_left: #same again


        if ball["rect"].colliderect(player["rect"]):
            if ball["rect"].centerx < player["rect"].centerx:
                ball_down_left = False
                ball_up_left = True
            if ball["rect"].centerx > player["rect"].centerx:
                ball_down_left = False
                ball_up_right = True

    if ball_down_left: #same again

        if ball["rect"].bottom < WINDOWHEIGHT:
            if ball["rect"].left > 0:
                ball["rect"].bottom += BALLMOVESPEED
                ball["rect"].left -= BALLMOVESPEED
            else:
                ball_down_left = False
                ball_down_right = True
        else:
            ball_down_left = False
            ball_up_left = True

    if ball["rect"].bottom == WINDOWHEIGHT:
        lives -= 1
        if lives == 0:
            print "you lose!"
            break

    pygame.draw.rect(window_surface, player["colour"], player["rect"])
    pygame.draw.rect(window_surface, ball["colour"], ball["rect"])
    for brick in bricks:
        pygame.draw.rect(window_surface, brick["colour"], brick["rect"])

    print "ball up left, ball up right, ball down left, ball down right", ball_up_left, ball_up_right, ball_down_left, ball_down_right

    pygame.display.update()
    main_clock.tick(40)

