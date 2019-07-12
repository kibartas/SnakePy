#!/bin/python

import pygame
import random
import time
import pprint
import socket
import datetime

snake_move_by_pixels = 10
snake_block_size = 10
screen_size = (480, 480)
apple_size = 8
collision = True
apple_color = (0, 255, 0)
default_game_speed = 0.08
game_slow_by = 0.001
game_speed = default_game_speed
score_block_height = 120
score = 0
white = (255, 255, 255)
black = (0, 0, 0)

def textToScreen(screen, text, x = 30, y = 30, size = 50, color = white, font_type = 'BillionaireMediumGrunge.ttf'):
    try:
        screen.fill((0, 0, 0), pygame.Rect(x, y, size+size, size))
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except e:
        print('Font Error')
        raise e


def snakeHeadCollideApple(screen, apple_block, snake_blocks, snake_head_coordinates, snake_head_block):
    global game_speed, score
    screen.fill((0, 0, 0), apple_block)
    snake_blocks.append(snake_head_block.copy())
    #print('Apple eaten' + str(apple_color))
    snake_head_coordinates = spawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
    #print('You ate an apple')
    apple_block = spawnApple(screen, snake_blocks, snake_head_block)
    game_speed -= game_slow_by
    score += 1
    textToScreen(screen, score)
    print('Your score is now', score)
    return (apple_block, snake_head_coordinates)

def setNewDirection(direction, directionsDict):
    directionsDict = dict.fromkeys(directionsDict, False)
    directionsDict[direction] = True
    return directionsDict

def spawnApple(screen, snake_blocks, snake_head_block):
    apple_block_coordinates = (random.randint(apple_size, (screen_size[0]-apple_size)//snake_block_size)*snake_block_size,
                               random.randint(apple_size, (screen_size[1]-apple_size)//snake_block_size)*snake_block_size+score_block_height)
    apple_block = pygame.Rect(apple_block_coordinates, (apple_size, apple_size))
    
    while True:
        for i in range(0, len(snake_blocks)):
            if snake_blocks[i].colliderect(apple_block) or snake_head_block.colliderect(apple_block):
                apple_block_coordinates = (random.randint(apple_size, (screen_size[0]-apple_size)//snake_block_size)
                                            *snake_block_size, random.randint(apple_size, (screen_size[1]-apple_size)
                                            //snake_block_size)*snake_block_size+score_block_height)
                apple_block = pygame.Rect(apple_block_coordinates, (apple_size, apple_size))
                i = 0
                
        break
    #print('Apple block coordinates' + str(apple_block_coordinates))
    apple_block = pygame.Rect(apple_block_coordinates, (apple_size, apple_size))
    screen.fill(apple_color, apple_block)
    pygame.display.update()
    return apple_block

def initSnake(screen, snake_block):
    screen.fill((255, 255, 255), snake_block)
    screen.fill((0, 0, 0), snake_block)

def spawnLeadBlocks(screen, snake_blocks, snake_head_coordinates):
    lowestIndex = 0
    for i in range(0, len(snake_blocks)):
        index = -(snake_block_size//snake_move_by_pixels)*(i+1)
        snake_blocks[i].left, snake_blocks[i].top = snake_head_coordinates[index]
        screen.fill((255, 0, 0), snake_blocks[i]) 
    return snake_head_coordinates[-(snake_block_size//snake_move_by_pixels)*(len(snake_blocks)+1):]

def despawnLeadBlocks(screen, snake_blocks, snake_head_coordinates):
    for i in range(0, len(snake_blocks)):
        snake_blocks[i].left, snake_blocks[i].top = snake_head_coordinates[-(snake_block_size//snake_move_by_pixels)*(i+1)]
        screen.fill((0, 0, 0), snake_blocks[i]) 
    return snake_head_coordinates[-(snake_block_size//snake_move_by_pixels)*(len(snake_blocks)+1):]

def snakeCollision(snake_blocks, snake_head_block):
    if collision == False:
        return False
    for block in snake_blocks:
        if block.colliderect(snake_head_block):
            return True
    if (snake_head_block.top >= screen_size[1]+score_block_height or snake_head_block.left >= screen_size[0]
            or snake_head_block.left < 0 or snake_head_block.top < score_block_height):
        return True
    return False 

def theGame(screen):
    global game_speed, score
    running = True
    snake_head_block = pygame.Rect(screen_size[0]/2, screen_size[1]/2, snake_block_size, snake_block_size)
    initSnake(screen, snake_head_block)
    apple_block = spawnApple(screen, (), snake_head_block)
    directions = {'Up': True, 'Down': False, 'Right': False, 'Left': False}

    hiscore_file = open('hiscores.txt', 'r')
    #hiscores_string = hiscore_file.read()
    hiscores = hiscore_file.read().split('\n')
    if hiscores != ['']:
        hiscores = hiscores[:-1]
        hiscores = [x.split(' ')[1:] for x in hiscores]
        for i in range(0, len(hiscores)):
            hiscores[i][1] = int(hiscores[i][1])
        hiscores = sorted(hiscores, key=lambda hiscore: hiscore[1], reverse=True)
        hiscore = hiscores[0][1]
    else:
        hiscores = []
        hiscore = 0
    screen.fill(black, pygame.Rect(0, 0, screen_size[0], score_block_height-1))
    textToScreen(screen, score)
    textToScreen(screen, 'Current hiscore is: ' + str(hiscore), 150, 0, 40) 

    screen.fill(white, pygame.Rect(0, 119, screen_size[0], 1))

    directionJustSet = False
    snake_head_coordinates = []
    snake_blocks = []
    coordinates = open('appleAndSnake.txt', 'a')
    while running:
        #coordinates.write('Snake' + (str((snake_head_block.left, snake_head_block.top))))
        #coordinates.write('Apple' + (str((apple_block.left, apple_block.top))))
        print('Snake' + (str((snake_head_block.left, snake_head_block.top))))
        print('Apple' + (str((apple_block.left, apple_block.top))))
        snake_head_coordinates.append((snake_head_block.left, snake_head_block.top))
        #print(snake_head_coordinates[-1])
        time.sleep(game_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if directions['Up'] == True or directions['Down'] == True:
                        continue
                    snake_head_block.top -= snake_move_by_pixels
                    directions = setNewDirection('Up', directions)
                    directionJustSet = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if directions['Left'] == True or directions['Right'] == True:
                        continue
                    snake_head_block.left -= snake_move_by_pixels
                    directions = setNewDirection('Left', directions)
                    directionJustSet = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if directions['Right'] == True or directions['Left'] == True:
                        continue
                    snake_head_block.left += snake_move_by_pixels
                    directions = setNewDirection('Right', directions)
                    directionJustSet = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if directions['Down'] == True or directions['Up'] == True:
                        continue
                    snake_head_block.top += snake_move_by_pixels
                    directions = setNewDirection('Down', directions)
                    directionJustSet = True
                elif event.key == pygame.K_SPACE:
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    paused = False 
                                    break 
                if snake_head_block.colliderect(apple_block):
                    apple_block, snake_head_coordinates = snakeHeadCollideApple(
                            screen, apple_block,
                            snake_blocks, snake_head_coordinates,
                            snake_head_block)
                if snakeCollision(snake_blocks, snake_head_block) == True:
                    running = False
                    break 
                screen.fill((255, 255, 255), snake_head_block)
                snake_head_coordinates = spawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
                #updateSnakeBlocks(screen, snake_head_coordinates, snake_blocks)
                pygame.display.update()
                screen.fill((0, 0, 0), snake_head_block)
                snake_head_coordinates = despawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('No')
        if running == False:
            break
        if directionJustSet == True:
            directionJustSet = False
            continue
        if directions['Up'] == True:
            snake_head_block.top -= snake_move_by_pixels
        elif directions['Down'] == True:
            snake_head_block.top += snake_move_by_pixels
        elif directions['Right'] == True:
            snake_head_block.left += snake_move_by_pixels
        elif directions['Left'] == True:
            snake_head_block.left -= snake_move_by_pixels
        if snake_head_block.colliderect(apple_block):
            apple_block, snake_head_coordinates = snakeHeadCollideApple(screen, apple_block,
                                                                        snake_blocks, snake_head_coordinates,
                                                                        snake_head_block)
        if snakeCollision(snake_blocks, snake_head_block) == True:
            print('You failed')
            break 
        snake_head_coordinates = spawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
        screen.fill((255, 255, 255), snake_head_block)
        pygame.display.update()
        snake_head_coordinates = despawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
        screen.fill((0, 0, 0), snake_head_block)
    if score > hiscore:
        hiscores += [[socket.gethostname(), score, str(datetime.datetime.now())]]
        print(hiscores)
        hiscores = sorted(hiscores, key=lambda hiscore: hiscore[1], reverse=True)
        for i in range(0, len(hiscores)):
            hiscores[i][1] = str(hiscores[i][1])
        final_hiscore_string = ''
        counter = 1
        for hiscore in hiscores:
            final_hiscore_string += str(counter) + '. ' + ' '.join(hiscore)
            final_hiscore_string += '\n'
            counter += 1
        hiscore_file = open('hiscores.txt', 'w')
        hiscore_file.write(final_hiscore_string)
        hiscore_file.flush()
    score = 0
    despawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
    screen.fill((0, 0, 0), apple_block)
    #print('Apple block destroyed at ' + str((apple_block.left, apple_block.top)))
    screen.fill((0, 0, 0), snake_head_block)
    game_speed = default_game_speed

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_size[0], screen_size[1]+score_block_height))
    while True:
        theGame(screen)
    

if __name__ == "__main__":
    main()

