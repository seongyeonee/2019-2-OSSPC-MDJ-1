#!/usr/bin/env python
# coding: utf-8

# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
from mino import *
from random import *
from pygame.locals import *
from ui import *
from screeninfo import get_monitors


#화면크기 조정
screen_width = 0
screen_height = 0

for m in get_monitors():
    screen_width = int(m.width*0.7)
    screen_height = int(m.height*0.7)

# Define
#block_size = 17 # Height, width of single block
block_size = 25
width = 10 # Board width
height = 20 # Board height
framerate = 30 # Bigger -> Slower

pygame.init()
size = [screen_width, screen_height]
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")


# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

# draw single board
def draw_single_board(next, hold, score, level, goal):
    screen.fill(ui_variables.black)
    background_image()

    # Draw sidebar _ right
    #pygame.draw.rect(
    #    screen,
    #    ui_variables.white,
    #    Rect(screen_width*0.68, screen_height*0.1, 120, 500)
    #)

    # Draw sidebar _ left
    #pygame.draw.rect(
    #    screen,
    #    ui_variables.white,
    #    Rect(screen_width*0.24, screen_height*0.1, 120, 500)
    #)

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            # 기존 각각 310, 140
            dx = screen_width*0.692  + block_size * j
            dy = screen_height*0.27 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                #dx = 310 + block_size * j
                #dy = 50 + block_size * i
                dx = screen_width*0.252 + block_size * j
                dy = screen_height*0.27 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.DG_v_small.render("HOLD", 1, ui_variables.white)
    text_next = ui_variables.DG_v_small.render("NEXT", 1, ui_variables.white)
    text_score = ui_variables.DG_v_small.render("SCORE", 1, ui_variables.white)
    score_value = ui_variables.DG_v_small.render(str(score), 1, ui_variables.white)
    text_level = ui_variables.DG_v_small.render("LEVEL", 1, ui_variables.white)
    level_value = ui_variables.DG_v_small.render(str(level), 1, ui_variables.white)
    text_goal = ui_variables.DG_v_small.render("GOAL", 1, ui_variables.white)
    goal_value = ui_variables.DG_v_small.render(str(goal), 1, ui_variables.white)

    # Place texts
    #screen.blit(text_hold, (305, 14))
    #screen.blit(text_next, (305, 104))
    #screen.blit(text_score, (305, 194))
    #screen.blit(score_value, (305, 210))
    #screen.blit(text_level, (305, 254))
    #screen.blit(level_value, (310, 270))
    #screen.blit(text_goal, (305, 314))
    #screen.blit(goal_value, (310, 330))
    screen.blit(text_hold, (screen_width*0.25, screen_height*0.2))
    screen.blit(text_level, (screen_width*0.25, screen_height*0.5))
    screen.blit(level_value, (screen_width*0.25, screen_height*0.57))
    screen.blit(text_goal, (screen_width*0.25, screen_height*0.7))
    screen.blit(goal_value, (screen_width*0.25, screen_height*0.77))
    screen.blit(text_next, (screen_width*0.69, screen_height*0.2))
    screen.blit(text_score, (screen_width*0.69, screen_height*0.6))
    screen.blit(score_value, (screen_width*0.69, screen_height*0.67))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = screen_width*0.4 + block_size * x
            dy = screen_height*0.1 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

# Draw multi board
def draw_multi_board(next, hold, score, level, goal):
    screen.fill(ui_variables.black)
    background_image()

    """# Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(294, 0, 96, 374)
        #Rect(364, 0, 96, 374)
    )"""

    # Draw "VS mode" word
    show_V_multi = ui_variables.DG_big.render("V",1,ui_variables.red)
    show_S_multi = ui_variables.DG_big.render("S",1,ui_variables.red)
    show_m_multi = ui_variables.DG_70.render("m",1,ui_variables.red)
    show_o_multi = ui_variables.DG_70.render("o",1,ui_variables.red)
    show_d_multi = ui_variables.DG_70.render("d",1,ui_variables.red)
    show_e_multi = ui_variables.DG_70.render("e",1,ui_variables.red)
    
    screen.blit(show_V_multi, (screen_width*0.47, screen_height*0.05))
    screen.blit(show_S_multi, (screen_width*0.47, screen_height*0.19))
    screen.blit(show_m_multi, (screen_width*0.477, screen_height*0.38))
    screen.blit(show_o_multi, (screen_width*0.477, screen_height*0.46))
    screen.blit(show_d_multi, (screen_width*0.477, screen_height*0.56))
    screen.blit(show_e_multi, (screen_width*0.477, screen_height*0.64))

    # Draw "VS mode" line
    pygame.draw.line(screen, ui_variables.white,
                [screen_width * 0.457, screen_height * 0.001],
                [screen_width * 0.457, screen_height*0.89],2)

    pygame.draw.line(screen, ui_variables.white,
                [screen_width * 0.54, screen_height * 0.001],
                [screen_width * 0.54, screen_height*0.89],2)


    # Draw next mino_player1
    grid_n = tetrimino.mino_map[next - 1][0]
    grid_m = tetrimino.mino_map[next - 1][0]

    for x in range(4):
        for y in range(4):
            dx = screen_width*0.385 + block_size * 0.72 * x
            dy = screen_height*0.27 + block_size * 0.72 * y
            if grid_n[x][y] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[x][y]],
                    Rect(dx, dy, block_size * 0.7, block_size * 0.7)
                )
    # Draw next mino_player2
    for i in range(4):
        for j in range(4):
            di = screen_width*0.919 + block_size * 0.72 * j
            dj = screen_height*0.27 + block_size * 0.72 * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_m[i][j]],
                    Rect(di, dj, block_size*0.7, block_size*0.7)
                )
    

    # Draw hold mino_player1
    grid_h = tetrimino.mino_map[hold - 1][0]
    grid_i = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for x in range(4):
            for y in range(4):
                dx = screen_width*0.012 + block_size * 0.72 * x
                dy = screen_height*0.27 + block_size * 0.72 * y
                if grid_h[x][y] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[x][y]],
                        Rect(dx, dy, block_size * 0.7, block_size * 0.7)
                    )

    # Draw hold mino_player2
    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                di = screen_width*0.545 + block_size * 0.72 * j
                dj = screen_height*0.27 + block_size * 0.72 * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_i[i][j]],
                        Rect(di, dj, block_size * 0.7, block_size * 0.7)
                    )


    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.DG_v_small.render("HOLD", 1, ui_variables.white)
    text_next = ui_variables.DG_v_small.render("NEXT", 1, ui_variables.white)
    text_score = ui_variables.DG_v_small.render("SCORE", 1, ui_variables.white)
    score_value = ui_variables.DG_v_small.render(str(score), 1, ui_variables.white)
    text_level = ui_variables.DG_v_small.render("LEVEL", 1, ui_variables.white)
    level_value = ui_variables.DG_v_small.render(str(level), 1, ui_variables.white)
    text_goal = ui_variables.DG_v_small.render("GOAL", 1, ui_variables.white)
    goal_value = ui_variables.DG_v_small.render(str(goal), 1, ui_variables.white)

    # Place texts for player1
    screen.blit(text_hold, (screen_width*0.016, screen_height*0.2))
    screen.blit(text_level, (screen_width*0.01, screen_height*0.5))
    screen.blit(level_value, (screen_width*0.04, screen_height*0.57))
    screen.blit(text_goal, (screen_width*0.015, screen_height*0.7))
    screen.blit(goal_value, (screen_width*0.027, screen_height*0.77))
    screen.blit(text_next, (screen_width*0.385, screen_height*0.2))
    screen.blit(text_score, (screen_width*0.38, screen_height*0.6))
    screen.blit(score_value, (screen_width*0.391, screen_height*0.67))

    # Place texts for player2
    screen.blit(text_hold, (screen_width*0.562, screen_height*0.2))
    screen.blit(text_level, (screen_width*0.55, screen_height*0.5))
    screen.blit(level_value, (screen_width*0.58, screen_height*0.57))
    screen.blit(text_goal, (screen_width*0.56, screen_height*0.7))
    screen.blit(goal_value, (screen_width*0.578, screen_height*0.77))
    screen.blit(text_next, (screen_width*0.918, screen_height*0.2))
    screen.blit(text_score, (screen_width*0.92, screen_height*0.6))
    screen.blit(score_value, (screen_width*0.931, screen_height*0.67))

    # Draw board - original
    """for x in range(width):
        for y in range(height):
            dx = 107 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]]) """

    # Draw board - player1
    for x in range(width):
        for y in range(height):
            dx = screen_width*0.0922 + block_size * x
            dy = screen_height*0.0035 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

    # Draw board - player2
    for i in range(width):
        for j in range(height):
            di = screen_width*0.63 + block_size * i
            dj = screen_height*0.0035 + block_size * j
            draw_block(di, dj, ui_variables.t_color[matrix[i][j + 1]])

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

#background image
def background_image():
    background = pygame.image.load('../assets/images/backgroundimage.png')
    picture = pygame.transform.scale(background,(screen_width,int(screen_height/2)))
    screen.blit(picture,(0,int(screen_height/2)))

#manual image
def manual_image():
    manual = pygame.image.load('../assets/images/manual.png')
    picture2 = pygame.transform.scale(manual, (screen_width, int(screen_height)))
    #screen.blit(picture2,(0,int(screen_height)))
    screen.blit(picture2,(0,0))

# insert image x,y 이미지 위치, r이미지 가로 길이, c이미지 세로 길이
def insert_image(image, x, y, r, c):
    photo = pygame.transform.scale(image, (r, c))
    screen.blit(photo, (x, y))

# image
image_aco1 = pygame.image.load('../assets/images/aco1.png')
image_aco2 = pygame.image.load('../assets/images/aco2.png')
image_aco3 = pygame.image.load('../assets/images/aco3.png')
image_manual = pygame.image.load('../assets/images/manual.png')

# Initial values
blink = False
#start = False
start_single = False  # sinlge mode
start_multi = False  # multi mode
pause = False
done = False
game_over = False
show_score = False
show_manual = False
screen_Start = True
game_mode = False
score = 0
level = 1
goal = 1
bottom_count = 0
hard_drop = False

dx, dy = 3, 0 # Minos location status
rotation = 0 # Minos rotation status

mino = randint(1, 7) # Current mino
next_mino = randint(1, 7) # Next mino

hold = False # Hold status
hold_mino = -1 # Holded mino

name_location = 0
name = [65, 65, 65]

# mouse position
mousePos = pygame.mouse.get_pos()

with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

leaders = {}

for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])

leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)] # Board matrix

###########################################################
# Loop Start
###########################################################

while not done:
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                ########### single / multi 조건 달아야함 ###########
                if start_single == True:
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                elif start_multi == True:
                    draw_multi_board(next_mino, hold_mino, score, level, goal)

                pause_text = ui_variables.DG_70.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.DG_small.render("Press esc to continue", 1, ui_variables.white)

                #screen.blit(pause_text, (43, 100))
                screen.blit(pause_text, (screen_width*0.415, screen_height*0.35))
                if blink:
                    #screen.blit(pause_start, (40, 160))
                    screen.blit(pause_start, (screen_width*0.38, screen_height*0.6))
                    blink = False
                else:
                    blink = True
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            # pause 후 q 누르면 창 나가짐
                elif event.key == K_q:
                    done = True

    # Game screen
    # Start_single screen
    elif start_single:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                draw_single_board(next_mino, hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        #draw_board(next_mino, hold_mino, score, level, goal)
                        draw_single_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            # start = False
                            start_single = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                #Q누르면 창 나가짐
                elif event.key == K_q:
                    done = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    #draw_board(next_mino, hold_mino, score, level, goal)
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    #draw_board(next_mino, hold_mino, score, level, goal)
                    draw_single_board(next_mino, hold_mino, score, level, goal)

        pygame.display.update()

    # Start_multi screen
    elif start_multi:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)                
                draw_multi_board(next_mino, hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        #draw_board(next_mino, hold_mino, score, level, goal)
                        draw_multi_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            # start = False
                            start_multi = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                #Q누르면 창 나가짐
                elif event.key == K_q:
                    done = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    #draw_board(next_mino, hold_mino, score, level, goal)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    #draw_board(next_mino, hold_mino, score, level, goal)
                    draw_multi_board(next_mino, hold_mino, score, level, goal)

        pygame.display.update()
    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.DG_70.render("GAME OVER", 1, ui_variables.white)
                #over_text_2 = ui_variables.DG_60.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.DG_v_small.render("Press return to continue", 1, ui_variables.white)

                #mode 따른 종료
                if start_single == True:
                    draw_single_board(next_mino, hold_mino, score, level, goal)
                elif start_multi == True:
                    draw_multi_board(next_mino, hold_mino, score, level, goal)

                #screen.blit(over_text_1, (58, 75))
                #screen.blit(over_text_2, (62, 105))
                screen.blit(over_text_1, (screen_width*0.37, screen_height*0.2))
                #screen.blit(over_text_2, (screen_width*0.42, screen_height*0.43))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                #screen.blit(name_1, (65, 147))
                #screen.blit(name_2, (95, 147))
                #screen.blit(name_3, (125, 147))
                screen.blit(name_1, (screen_width*0.4, screen_height*0.5))
                screen.blit(name_2, (screen_width*0.5, screen_height*0.5))
                screen.blit(name_3, (screen_width*0.6, screen_height*0.5))

                if blink:
                    #screen.blit(over_start, (32, 195))
                    screen.blit(over_start, (screen_width*0.38, screen_height*0.7))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (screen_width*0.4, screen_height*0.52))
                    elif name_location == 1:
                        screen.blit(underbar_2, (screen_width*0.5, screen_height*0.52))
                    elif name_location == 2:
                        screen.blit(underbar_3, (screen_width*0.6, screen_height*0.52))
                    blink = True

                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_q:
                    done = True

    elif game_mode:

        for event in pygame.event.get():

            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                # Q누르면 창 나가짐
                if event.key == K_q:
                    done = True
                #space누르면 매뉴얼 창으로
                elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_e]:
                    start_single = True
                    level = 1
                    goal = level * 5
                elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_r]:
                    level = 5
                    start_single = True
                    goal = level * 5
                elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_t]:
                    level = 10
                    start_single = True
                    goal = level * 5

                elif pygame.key.get_pressed()[K_m] and pygame.key.get_pressed()[K_e]:
                    start_mutlti= True
                    level = 1
                    goal = level * 5
                elif pygame.key.get_pressed()[K_m] and pygame.key.get_pressed()[K_r]:
                    level = 5
                    goal = level * 5
                    start_multi = True
                elif pygame.key.get_pressed()[K_m] and pygame.key.get_pressed()[K_t]:
                    level = 10
                    start_multi = True
                    goal = level * 5


            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                screen.fill(ui_variables.black)
                background_image()

                game_mode_title = ui_variables.DG_small.render("게임옵션설정(두개의 키를 동시에 눌러주세요!)", 1, ui_variables.white)
                game_mode_choice = ui_variables.DG_v_small.render("게임모드설정", 1, ui_variables.white)
                game_mode_speed = ui_variables.DG_v_small.render("게임속도설정", 1, ui_variables.white)

                game_mode_single = ui_variables.DG_v_small.render("● Single 모드 (S키)", 1, ui_variables.white)
                game_mode_single_des = ui_variables.DG_v_small.render("혼자서 재미있게 하기!!", 1, ui_variables.white)
                game_mode_multi = ui_variables.DG_v_small.render("● Multi 모드 (M키)", 1, ui_variables.white)
                game_mode_multi_des = ui_variables.DG_v_small.render("둘이서 재미있게 하기!!", 1, ui_variables.white)

                game_speed_easy = ui_variables.DG_v_small.render("● 아코 모드(E키)", 1, ui_variables.white)
                game_speed_normal = ui_variables.DG_v_small.render("● 엉아코 모드(R키)", 1, ui_variables.white)
                game_speed_hard = ui_variables.DG_v_small.render("● 졸업코 모드(T키)", 1, ui_variables.white)

                game_speed_easy_des = ui_variables.DG_v_small.render("EASY 모드!", 1, ui_variables.white)
                game_speed_normal_des = ui_variables.DG_v_small.render("NORMAL 모드!!", 1, ui_variables.white)
                game_speed_hard_des = ui_variables.DG_v_small.render("HARD 모드!!!", 1, ui_variables.white)

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.055)],
                [screen_width,int(screen_height*0.055)],2)

                screen.blit(game_mode_title, (int(screen_width*0.1)+int(int(screen_width*0.3)*0.4), int(screen_height*0.065)))

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.125)],
                [screen_width,int(screen_height*0.125)],2)

                pygame.draw.rect(screen, ui_variables.white, [int(screen_width*0.175), int(screen_height*0.2), int(screen_width*0.2), int(screen_height*0.075)], 2)
                pygame.draw.rect(screen, ui_variables.white, [int(screen_width*0.625), int(screen_height*0.2), int(screen_width*0.2), int(screen_height*0.075)], 2)

                screen.blit(game_mode_choice, (int(screen_width*0.198), int(screen_height*0.215)))
                screen.blit(game_mode_speed, (int(screen_width*0.655), int(screen_height*0.215)))

                screen.blit(game_mode_single, (int(screen_width*0.15), int(screen_height*0.35)))
                screen.blit(game_mode_multi, (int(screen_width*0.15), int(screen_height*0.55)))
                screen.blit(game_mode_single_des, (int(screen_width*0.179), int(screen_height*0.4)))
                screen.blit(game_mode_multi_des, (int(screen_width*0.179), int(screen_height*0.6)))

                screen.blit(game_speed_easy, (int(screen_width*0.6), int(screen_height*0.3)))
                screen.blit(game_speed_normal, (int(screen_width*0.6), int(screen_height*0.45)))
                screen.blit(game_speed_hard, (int(screen_width*0.6), int(screen_height*0.6)))

                screen.blit(game_speed_easy_des, (int(screen_width*0.65), int(screen_height*0.35)))
                screen.blit(game_speed_normal_des, (int(screen_width*0.65), int(screen_height*0.5)))
                screen.blit(game_speed_hard_des, (int(screen_width*0.65), int(screen_height*0.65)))

                insert_image(image_aco1, int(screen_width*0.79), int(screen_height*0.295), int(screen_width*0.1), int(screen_height*0.1))
                insert_image(image_aco2, int(screen_width*0.8), int(screen_height*0.445), int(screen_width*0.1), int(screen_height*0.1))
                insert_image(image_aco3, int(screen_width*0.8), int(screen_height*0.595), int(screen_width*0.1), int(screen_height*0.1))



            pygame.display.update()

    # Manual screen
    elif show_manual:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_mode = True

                elif event.key == K_q:
                    done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                screen.fill(ui_variables.black)
                manual_image()

                show_score_manual = ui_variables.DG_small.render("Manual", 1, ui_variables.white)
                show_desc1_manual = ui_variables.DGM23.render("Pytris는 테트리스 게임으로 총 7가지 모양의 블록이 위에서 아래로", 1, ui_variables.white)
                show_desc2_manual = ui_variables.DGM23.render("떨어질 때 블록을 회전, 이동, 낙하 시켜 빈 곳으로 블록을 끼워 넣어", 1, ui_variables.white)
                show_desc3_manual = ui_variables.DGM23.render("한 라인을 채우면 라인이 제거되면서 점수를 얻는 방식입니다.", 1, ui_variables.white)

                #show_function_manual = ui_variables.DGM23.render("기능",1, ui_variables.white)
                #show_key_manual = ui_variables.DGM23.render("키(싱글/멀티)",1, ui_variables.white)

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.055)],
                [screen_width,int(screen_height*0.055)],2)

                screen.blit(show_score_manual, (int(screen_width*0.3)+int(int(screen_width*0.3)*0.5), int(screen_height*0.06)))

                screen.blit(show_desc1_manual, (int(screen_width*0.05)+int(int(screen_width*0.1)*0.5), int(screen_height*0.15)))
                screen.blit(show_desc2_manual, (int(screen_width*0.05)+int(int(screen_width*0.1)*0.5), int(screen_height*0.2)))
                screen.blit(show_desc3_manual, (int(screen_width*0.05)+int(int(screen_width*0.1)*0.5), int(screen_height*0.25)))

                #screen.blit(show_function_manual, (int(screen_width*0.1)+int(int(screen_width*0.1)*0.5), int(screen_height*0.3)))
                #screen.blit(show_key_manual, (int(screen_width*0.23)+int(int(screen_width*0.1)*0.5), int(screen_height*0.3)))

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.125)],
                [screen_width,int(screen_height*0.125)],2)

                title_start = ui_variables.DGM23.render("<Press space to start>", 1, ui_variables.white)
                screen.blit(title_start, (screen_width*0.37, screen_height*0.75))

            pygame.display.update()

    # Show score
    elif show_score:

        for event in pygame.event.get():

            if event.type == QUIT:
                done = True

            elif event.type == KEYDOWN:
                # Q누르면 창 나가짐
                if event.key == K_q:
                    done = True
                #space누르면 매뉴얼 창으로
                elif event.key == K_SPACE:
                    show_manual = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                screen.fill(ui_variables.black)
                background_image()

                show_button_right = ui_variables.DGM23.render("<Press space to start>", 1, ui_variables.black)
                show_score_title = ui_variables.DG_small.render("Ranking", 1, ui_variables.black)

                show_score_list = list()

                for i in range(0,10):
                    j=0
                    temp = ui_variables.DG_small.render('%2d' % ((i+1))+'등 '+'{:>6s}'.format(leaders[i][j]) + '   ' + '{:<8s}'.format(str(leaders[i][j+1])), 1, ui_variables.white)
                    show_score_list.append(temp)

                show_name_y = int(screen_height*0.17)
                prop = (show_name_y*0.3)

                for element in show_score_list:
                    screen.blit(element, (int(screen_width*0.3)+int(int(screen_width*0.3)*0.25), show_name_y))
                    show_name_y += prop

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.055)],
                [screen_width,int(screen_height*0.055)],2)

                screen.blit(show_score_title, (int(screen_width*0.3)+int(int(screen_width*0.3)*0.5), int(screen_height*0.065)))

                pygame.draw.line(screen, ui_variables.white,
                [0, int(screen_height*0.125)],
                [screen_width,int(screen_height*0.125)],2)

                #pygame.draw.rect(screen, ui_variables.white, [int(screen_width*0.32)+int(int(screen_width*0.32)*0.45),show_name_y+prop,int(screen_width*0.07),int(screen_height*0.06)])
                #screen.blit(show_button_right, (int(screen_width*0.33)+int(int(screen_width*0.33)*0.2), show_name_y+prop))
                screen.blit(show_button_right, (screen_width*0.37, screen_height*0.75))

            pygame.display.update()

    # Start screen
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    show_score=True
            #Q 누르면 창 나가짐
                elif event.key == K_q:
                    done = True




        # pygame.time.set_timer(pygame.USEREVENT, 300)
        screen.fill(ui_variables.white)
        background_image()

        insert_image(image_aco1, screen_width*0.52, screen_height*0.29, 150, 130)
        insert_image(image_aco2, screen_width*0.65, screen_height*0.22, 180, 180)
        insert_image(image_aco3, screen_width*0.8, screen_height*0.18, 210, 210)


        title = ui_variables.DG_big.render("PYTRIS", 1, ui_variables.black)
        title_uni = ui_variables.DG_small.render("in DGU", 1, ui_variables.black)
        title_start = ui_variables.DGM23.render("<Press space to start>", 1, ui_variables.white)
        title_info = ui_variables.DGM13.render("Copyright (c) 2017 Jason Kim All Rights Reserved.", 1, ui_variables.white)

        if blink:
            screen.blit(title_start, (92, 195))
            blink = False
        else:
            blink = True

        screen.blit(title, (screen_width*0.04, screen_height*0.3))
        screen.blit(title_uni, (screen_width*0.36, screen_height*0.3))
        screen.blit(title_start, (screen_width*0.37, screen_height*0.55))
        screen.blit(title_info, (screen_width*0.35, screen_height*0.93))


        if not show_score:
            pygame.display.update()
            clock.tick(3)

        #여기에 버튼 만들고 그걸 클릭하면 show_score = True로 해줘야해요!

pygame.quit()
