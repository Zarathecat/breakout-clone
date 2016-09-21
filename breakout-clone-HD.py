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
BALLMOVESPEED = 7

WHITE = (255, 255, 255)
GREY = (50, 50, 50)
BLUE = (0, 0, 255)
DARKBLUE = (0,0, 50)
CYAN = (0, 255, 255)
DARKCYAN = (0, 50,50)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKYELLOW = (50, 50, 0)
BLACK = (20,20,20)#slightly off-black so we can make out the borders in fullscreen
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (50, 0, 0)
ORANGE = (255, 175, 0)
DARKORANGE = (50, 25, 0)


pygame.init()

window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)

window_rect = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
pygame.mouse.set_visible(False)

basic_font = pygame.font.SysFont(None, 48)

def level_colour(level):
    if level == 1:
        return BLACK
    if level == 2:
        return DARKRED
    if level == 3:
        return DARKORANGE
    if level == 4:
        return DARKYELLOW
    if level == 5:
        return DARKCYAN
    if level == 6:
        return DARKBLUE
    if level == 7:
        return GREY
    return BLACK

def end_game():

    pygame.quit()
    sys.exit()

bricks = []

redbrick = pygame.image.load('pics/red-brick2.png')
orangebrick = pygame.image.load('pics/orange-brick2.png')
yellowbrick = pygame.image.load('pics/yellow-brick2.png')
greenbrick = pygame.image.load('pics/green-brick2.png')
cyanbrick = pygame.image.load('pics/cyan-brick2.png')
bluebrick = pygame.image.load('pics/blue-brick2.png')
purplebrick = pygame.image.load('pics/purple-brick2.png')
ballimage = pygame.image.load('pics/ball-1.png')
ballimage = pygame.transform.scale(ballimage, (10,10))
paddle = pygame.image.load('pics/paddle.png')

def make_bricks(level):
#todo: tidy these.
    for i in range(15): #starts at 0
        brick_1 = {"rect":pygame.Rect(i*40, 20, 39, 10), "colour":RED, "image":redbrick}
        brick_2 = {"rect":pygame.Rect(i*40+10, 40, 39, 10), "colour":ORANGE,"image":orangebrick}
        brick_3 = {"rect":pygame.Rect(i*40, 60, 39, 10), "colour":YELLOW, "image":yellowbrick}
        brick_4 = {"rect":pygame.Rect(i*40+10, 80, 39, 10), "colour":GREEN, "image":greenbrick}
        brick_5 = {"rect":pygame.Rect(i*40, 100, 39, 10), "colour":CYAN, "image":cyanbrick}
        brick_6 = {"rect":pygame.Rect(i*40+10, 120, 39, 10), "colour":BLUE, "image":bluebrick}
        brick_7 = {"rect":pygame.Rect(i*40, 140, 39, 10), "colour":WHITE, "image":purplebrick}

        #get an extra line of bricks per level. they go downwards since easier to hit lower ones

        if level >= 1:
	    bricks.append(brick_7)

        if level >=2:
	    bricks.append(brick_6)

        if level >=3:
	    bricks.append(brick_5)

        if level >=4:
	    bricks.append(brick_4)
 
        if level >=5:
	    bricks.append(brick_3)

        if level >=6:
	    bricks.append(brick_2)

        if level >= 7:
	    bricks.append(brick_7)

def play_music(level):

    pygame.mixer.music.stop()

    if level == 1:
       music = 'music/breakout-1.wav'

    if level == 2:
       music = 'music/breakout-2.wav'

    if level == 3:
       music = 'music/breakout-3.wav'

    if level == 4:
       music = 'music/breakout-4.wav'

    if level == 5:
       music = 'music/breakout-5.wav'

    if level == 6:
       music = 'music/breakout-6.wav'

    if level >= 7:
       music = 'music/breakout-7.wav'

    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1, 0.0)


def await_input():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event == QUIT:
                    end_game()
                return

level = 1
lives = 0

while True:
    make_bricks(level)
    play_music(level)
    if level == 8:
        print "YOU WIN!"
        end_game()
    if lives > 2: #now you get an extra life if you lose no lives in a level
        lives += 1
    else:
        lives = 3
    FPS = level*5 + 35 #todo: have bgm with complementary tempo. this will start at 40fps and increase by 5 each win

    #player and ball in loop so that it doesn't initialise with the player in a location from which they can't hit the ball
    player = {"rect":pygame.Rect(0, WINDOWHEIGHT-20, 80, 20), "colour":GREEN}
    ball = {"rect":pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 10,10), "colour":MAGENTA}#make ball big just to see what happens
    
    move_player_right = move_player_left = False

    ball_up_right = ball_up_left = ball_down_right = ball_down_left = False

    player_turbo = False

    ball_down_left = True #arbitrarily selected start dir
    wait_text = basic_font.render('Press a key to play!', True, WHITE)
    window_surface.blit(wait_text, window_rect)
    pygame.display.update()

    await_input()


    while True:

        window_surface.fill(level_colour(level))
        lives_display = basic_font.render('Lives: %d' % lives, True, WHITE)
        lives_rect = lives_display.get_rect()
        lives_rect.bottom = WINDOWHEIGHT
        lives_rect.right = WINDOWWIDTH #on right so not hidden by paddle at game start


        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   end_game()
                if event.key == K_SPACE:
                   PLAYERMOVESPEED = PLAYERMOVESPEED * 2
                   player_turbo = True

                if event.key == ord('y'):
                   FPS = 180

                if event.key == K_LEFT:
                    move_player_right = False
                    move_player_left = True

                if event.key == K_RIGHT:
                    move_player_left = False
                    move_player_right = True

            if event.type == KEYUP:
                if event.key == K_SPACE:
                    if player_turbo:
                        PLAYERMOVESPEED = PLAYERMOVESPEED /2 #this is a bit glitchy and has same effect on 'await input' menu...
                    player_turbo = False

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
                 ball_down_right = False
                 if move_player_right:
                     ball_up_right = True
                     ball["rect"].right += 1

                 elif move_player_left:
                     ball_up_right = False
                     ball_up_left = True

                 else:
                     ball_up_left = False
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
                lives -= 1


        if ball_down_left:

            for brick in bricks[:]:
                if brick["rect"].colliderect(ball["rect"]):
                    bricks.remove(brick)
                    ball_down_left = False
                    ball_up_left = True

        if ball_down_left: #same again


            if ball["rect"].colliderect(player["rect"]):
                ball_down_left = False
                if move_player_left:
                    ball_up_left = True
                    ball["rect"].left -=1

                elif move_player_right:
                    ball_up_left = False
                    ball_up_right = True

                else:
                    ball_up_right = False
                    ball_up_left = True



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
                lives -= 1

        if lives == 0:
            window_surface.fill(BLACK)
            game_over = basic_font.render('Game Over!', True, WHITE)
            game_over_rect = game_over.get_rect()
            game_over_rect.centerx = window_rect.centerx
            game_over_rect.centery = window_rect.centery
            window_surface.blit(game_over, game_over_rect)
            pygame.display.update()
            print "you lose!"
            break

        window_surface.blit(lives_display, lives_rect)
        window_surface.blit(paddle, player["rect"])
        window_surface.blit(ballimage, ball["rect"])
        for brick in bricks:
            window_surface.blit(brick["image"], brick["rect"])#prev used brick["colour"] in place of brick["image"]


        pygame.display.update()
        if len(bricks) < 1:
            window_surface.fill(BLACK)
            you_win = basic_font.render('You Win!', True, WHITE)
            you_win_rect = you_win.get_rect()
            you_win_rect.centerx = window_rect.centerx
            you_win_rect.centery = window_rect.centery
            window_surface.blit(you_win, you_win_rect)
            pygame.display.update()

            print "You win!"
            level +=1
            break

        main_clock.tick(FPS)

