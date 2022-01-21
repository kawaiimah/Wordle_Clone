# -*- coding: utf-8 -*-

import sys
import random
import pygame
pygame.init()

board = pygame.display.set_mode((250, 400))
pygame.display.set_caption('Wordle_Clone')

white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
yellow = (245,190,0)
grey = (200,200,200)

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

keyboard_font = pygame.font.SysFont('arial', 25)
tile_font = pygame.font.SysFont('arial', 40)

try:
    with open('puzzle.txt') as f:
        puzzle = set(f.read().split())
    puzzle = [x.upper() for x in puzzle if len(x)==5]
    
    with open('allowed.txt') as f:
        allowed = set(f.read().split())
    allowed = [x.upper() for x in allowed if len(x)==5] + puzzle
except:
    sys.exit()

if not puzzle:
    sys.exit()

def update_board(attempt,guess,letters,past,secret):
    
    board.fill(white)
    
    for i in range(6):
        for j in range(5):
            tile = pygame.Rect(2+j*50,2+i*50,46,46)
            pygame.draw.rect(board,black,tile,2)
    
    if guess:
        for i,c in enumerate(list(guess)):
            tile_char = tile_font.render(c,1,black)
            char_tile = tile_char.get_rect()
            char_tile.center = (25+i*50, 25+attempt*50)
            board.blit(tile_char, char_tile)
            
    if past:
        for i,w in enumerate(past):
            for j,c in enumerate(list(w)):
                if c not in secret:
                    color = grey
                elif c == secret[j]:
                    color = green
                else:
                    color = yellow
                tile_char = tile_font.render(c,1,color)
                char_tile = tile_char.get_rect()
                char_tile.center = (25+j*50, 25+i*50)
                board.blit(tile_char, char_tile)
    
    for i,c in enumerate(list('QWERTYUIOP')):
        keyboard_char = keyboard_font.render(c,1,letters[c])
        char_tile = keyboard_char.get_rect()
        char_tile.center = (18+i*24, 320)
        board.blit(keyboard_char, char_tile)
        
    for i,c in enumerate(list('ASDFGHJKL')):
        keyboard_char = keyboard_font.render(c,1,letters[c])
        char_tile = keyboard_char.get_rect()
        char_tile.center = (26+i*24, 350)
        board.blit(keyboard_char, char_tile)
    
    for i,c in enumerate(list('ZXCVBNM')):
        keyboard_char = keyboard_font.render(c,1,letters[c])
        char_tile = keyboard_char.get_rect()
        char_tile.center = (50+i*24, 380)
        board.blit(keyboard_char, char_tile)
    
    pygame.display.update()

def update_letters(guess,secret,letters):
    for i,c in enumerate(list(guess)):
        if letters[c] != green:
            if c not in secret:
                letters[c] = grey
            elif c == secret[i]:
                letters[c] = green
            else:
                letters[c] = yellow
    return letters
    
def main():
    
    run = True
    
    letters = {}
    for c in alphabet:
        letters[c] = black
    
    secret = random.choice(puzzle)
    
    attempt = 0
    guess = ''
    past = []
    
    while run:
        
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if (event.unicode in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or event.unicode in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()) and len(guess) < 5:
                    guess += event.unicode.upper()
                if event.key == pygame.K_BACKSPACE and len(guess) > 0:
                    guess = guess[:-1]
                if event.key == pygame.K_RETURN and len(guess) == 5:
                    if guess in allowed:
                        past.append(guess)
                        attempt += 1
                        if guess == secret or attempt > 5:
                            run = False
                        else:
                            letters = update_letters(guess,secret,letters)
                        guess = ''
        
        update_board(attempt,guess,letters,past,secret)
    
    pygame.draw.rect(board,white,pygame.Rect(0,300,250,100))
    if past[-1] == secret:
        message = keyboard_font.render('Congrats!',1,green)
    else:
        message = keyboard_font.render(secret,1,green)
    message_tile = message.get_rect()
    message_tile.center = (125, 320)
    board.blit(message, message_tile)
    new = keyboard_font.render('New puzzle in',1,black)
    new_tile = new.get_rect()
    new_tile.center = (125, 350)
    board.blit(new, new_tile)
    for i in range(5,0,-1):
        xseconds = keyboard_font.render(f'{i} seconds...',1,black)
        xseconds_tile = xseconds.get_rect()
        xseconds_tile.center = (125, 380)
        board.blit(xseconds, xseconds_tile)
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.draw.rect(board,white,pygame.Rect(0,365,250,350))
    
    main()
    
    
if __name__ == "__main__":
    main()