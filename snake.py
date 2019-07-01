#!/bin/python

import pygame
import random
import time
import pprint

snake_move_by_pixels = 10
snake_block_size = 10
screen_size = (480, 480)
apple_size = 8
collision = True
apple_color = (0, 255, 0)
default_game_speed = 0.05
game_slow_by = 0.0005
game_speed = default_game_speed
score = 0

def snakeHeadCollideApple(screen, apple_block, snake_blocks, snake_head_coordinates, snake_head_block):
    global game_speed, score
    screen.fill((0, 0, 0), apple_block)
    snake_blocks.append(snake_head_block.copy())
    print('Apple eaten' + str(apple_color))
    snake_head_coordinates = spawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
    print('You ate an apple')
    apple_block = spawnApple(screen, snake_blocks, snake_head_block)
    game_speed -= game_slow_by
    score += 1
    return (apple_block, snake_head_coordinates)

def setNewDirection(direction, directionsDict):
    directionsDict = dict.fromkeys(directionsDict, False)
    directionsDict[direction] = True
    return directionsDict

def spawnApple(screen, snake_blocks, snake_head_block):
    apple_block_coordinates = (random.randint(apple_size, (screen_size[0]-apple_size)//snake_block_size)*snake_block_size,
                               random.randint(apple_size, (screen_size[1]-apple_size)//snake_block_size)*snake_block_size)
    apple_block = pygame.Rect(apple_block_coordinates, (apple_size, apple_size))
    while True:
        for i in range(0, len(snake_blocks)):
            if snake_blocks[i].colliderect(apple_block) or snake_blocks[i].colliderect(snake_head_block):
                apple_block_coordinates = (random.randint(apple_size, (screen_size[0]-apple_size)//snake_block_size)
                                            *snake_block_size, random.randint(apple_size, (screen_size[1]-apple_size)
                                            //snake_block_size)*snake_block_size)
                apple_block = pygame.Rect(apple_block_coordinates, (apple_size, apple_size))
                i = 0
                
        break
    print('Apple block coordinates' + str(apple_block_coordinates))
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
    if (snake_head_block.top >= screen_size[0]-5 or snake_head_block.left >= screen_size[1]-5
            or snake_head_block.left < 0 or snake_head_block.top < 0):
        return True
    return False 

def theGame(screen):
    global game_speed
    score_font = pygame.font.Font('Super Plumber Brothers.ttf', 30)
    header_text = score_font.render('Score', True, (255, 255, 255))
    running = True
    snake_head_block = pygame.Rect(screen_size[0]/2, screen_size[1]/2, snake_block_size, snake_block_size)
    initSnake(screen, snake_head_block)
    apple_block = spawnApple(screen, (), snake_head_block)
    directions = {'Up': True, 'Down': False, 'Right': False, 'Left': False}
    directionJustSet = False
    snake_head_coordinates = []
    snake_blocks = []
    score = 0
    while running:
        print('Snake' + (str((snake_head_block.left, snake_head_block.top))))
        print('Apple' + (str((apple_block.left, apple_block.top))))
        snake_head_coordinates.append((snake_head_block.left, snake_head_block.top))
        #print(snake_head_coordinates[-1])
        time.sleep(game_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w:
                    if directions['Up'] == True or directions['Down'] == True:
                        continue
                    snake_head_block.top -= snake_move_by_pixels
                    directions = setNewDirection('Up', directions)
                    directionJustSet = True
                elif event.key == pygame.K_a:
                    if directions['Left'] == True or directions['Right'] == True:
                        continue
                    snake_head_block.left -= snake_move_by_pixels
                    directions = setNewDirection('Left', directions)
                    directionJustSet = True
                elif event.key == pygame.K_d:
                    if directions['Right'] == True or directions['Left'] == True:
                        continue
                    snake_head_block.left += snake_move_by_pixels
                    directions = setNewDirection('Right', directions)
                    directionJustSet = True
                elif event.key == pygame.K_s:
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
    despawnLeadBlocks(screen, snake_blocks, snake_head_coordinates)
    screen.fill((0, 0, 0), apple_block)
    #print('Apple block destroyed at ' + str((apple_block.left, apple_block.top)))
    screen.fill((0, 0, 0), snake_head_block)
    game_speed = default_game_speed

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    while True:
        theGame(screen)
    

if __name__ == "__main__":
    main()

