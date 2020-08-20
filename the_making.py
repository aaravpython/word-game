import pygame
import sys
import time
import random
from pygame.locals import *
from waiting import wait
from datetime import datetime

pygame.init()

size = [700, 700]
white = [255, 255, 255]
black = (0, 0, 0)
red = [255, 0, 0]
green = [32, 235, 21]
blue = [0, 0, 255]
lightblue = [82, 82, 255]
darkblue = [0, 0, 99]
score = 0
w_done = []
level = 1
level_file_map = {1 : 'Es_1.txt', 2 : 'E_2.txt', 3 : 'E_3.txt', 4 : 'easy.txt', 5 : 'H_1.txt', 6: 'H_2.txt', 7: 'H_3.txt', 8 : 'hard.txt'}
total_time = 10
lives = 3
screen = pygame.display.set_mode(size)
screen.fill(white)

font = pygame.font.Font('fonts/Lobster-Regular.ttf', 50)
font1 = pygame.font.Font('fonts/Lobster-Regular.ttf', 35)
font2 = pygame.font.Font('fonts/Lobster-Regular.ttf', 42)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def make_button(text, colour, left, up, size_up, size_left):
    pygame.draw.rect(screen, colour, (left, up, size_up, size_left))
    final_screen1 = font.render(text, True, black)
    final_screen1_rect = final_screen1.get_rect()
    final_screen1_rect.center = (left+int(size_up/2), up+int(size_left/2))
    screen.blit(final_screen1, final_screen1_rect)


def transition(colour, right_position, top_position):
    down_size = 1
    right_size = 1

    while right_position+right_size <=700 or top_position+down_size <=700 or right_position>=0 or top_position>=0:
        pygame.draw.rect(screen, colour, (right_position, top_position, down_size, right_size))
        time.sleep(0.001)
        right_position = right_position - 1
        top_position = top_position - 1
        down_size = down_size + 2
        right_size = right_size + 2
        pygame.display.update()


def replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring
    return s[:index] + newstring + s[index + 1:]


def find_Uscored():
    l = level_file_map[level]

    with open(l, "r") as fp:
        word_list = fp.readlines()
        num = 2

    word_list = [i.strip() for i in word_list]
    w_left = [i for i in word_list if i not in w_done]
    word_index = random.randint(0, len(w_left) - 1)
    w_to_show = w_left[word_index]
    w_done.append(w_to_show)
    char_idx = random.sample(range(0, len(w_to_show)), num)
    char_idx.sort(reverse=True)

    for i in char_idx:
        w_to_show = replacer(w_to_show, "_", i)

    new_screen(w_to_show, w_left[word_index])


def new_screen(w_to_show, correct_answer):
    global score
    global level
    global w_done
    global total_time
    global lives
    name = ''
    t = time.time()

    while True:
        screen.fill(green)

        make_button(f'WORD', blue, 270, 150, 150, 50)

        n_time = time.time()

        time_left = total_time- int(n_time-t)
        if time_left==0:
            lives-=1
            if lives == 0:
                last_s()
            else:
                find_Uscored()


        block7 = font1.render(f'time Left: {time_left}', True, black)
        rect7 = block7.get_rect()
        rect7.center = screen.get_rect().center[0] - 240, screen.get_rect().center[1] - 300

        block = font.render(w_to_show, True, black)
        rect = block.get_rect()
        rect.center = screen.get_rect().center[0], screen.get_rect().center[1] + 50

        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    print (name, correct_answer)
                    if name.strip() == correct_answer.strip():
                        if score % 5 == 0 and score != 0:
                            level +=1
                            total_time += 1
                        score += 1
                        find_Uscored()
                    elif name.strip() != correct_answer.strip():
                        lives -= 1
                        if lives == 0:
                            last_s()
                        else:
                            find_Uscored()

            elif evt.type == QUIT:
                exit()


        block2 = font1.render(f'score: {score}', True, black)
        rect2 = block2.get_rect()
        rect2.center = screen.get_rect().center[0] + 270, screen.get_rect().center[1] - 320
        screen.blit(block2, rect2)
        screen.blit(block, rect)

        block1 = font.render(name, True, black)
        rect1 = block1.get_rect()
        rect1.center = screen.get_rect().center[0],screen.get_rect().center[1]+150
        screen.blit(block1, rect1)
        screen.blit(block, rect)

        block5 = font1.render(f'level: {level}', True, black)
        rect5 = block5.get_rect()
        rect5.center = screen.get_rect().center[0] + 280, screen.get_rect().center[1] - 270
        screen.blit(block5, rect5)
        screen.blit(block, rect)
        screen.blit(block7, rect7)

        block3 = font1.render(f'lives: {lives}', True, black)
        rect3 = block3.get_rect()
        rect3.center = screen.get_rect().center[0] + 280, screen.get_rect().center[1] - 220
        screen.blit(block3, rect3)
        screen.blit(block, rect)
        screen.blit(block7, rect7)

        pygame.display.flip()
        pygame.display.update()



def last_s():
    screen.fill(lightblue)
    make_button(f'GAME OVER', darkblue, 230, 270, 250, 70)

    block4 = font.render(f'score: {score}', True, black)
    rect4 = block4.get_rect()
    rect4.center = screen.get_rect().center[0],screen.get_rect().center[1]+150
    screen.blit(block4, rect4)

    block6 = font.render(f'You Were On Level {level}', True, black)
    rect6 = block6.get_rect()
    rect6.center = screen.get_rect().center[0], screen.get_rect().center[1] + 250
    screen.blit(block6, rect6)

    pygame.display.flip()
    pygame.display.update()
    time.sleep(5)
    exit()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            time.sleep(1)
            sys.exit()

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if mouse[0]>280 and mouse[0]<(280+147):
        if mouse[1]>390 and mouse[1]<(390+63):
            make_button(f'START', lightblue, 280, 390, 154, 63)

        else:
            make_button(f'START', blue, 280, 390, 154, 63)

    else:
        make_button(f'START', blue, 280, 390, 154, 63)


    if click[0] == 1:
        if mouse[0] > 280 and mouse[0] < (280 + 147):
            if mouse[1] > 390 and mouse[1] < (390 + 63):
                transition(green, mouse[0]-1, mouse[1]-1)
                find_Uscored()

    pygame.display.update()

pygame.quit()