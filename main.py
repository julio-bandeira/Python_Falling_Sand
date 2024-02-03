import pygame
import numpy as np
import random
import sys

pygame.init()

original_size = [80, 80]
scale = 10
output_size = [(original_size[0]*scale), (original_size[1]*scale)]
button_pressed = False

frame_count = 0
hue_count = 0

matriz_areia = np.zeros(((original_size[0], original_size[1])))
matriz_cor = np.zeros(((original_size[0], original_size[1])))

def rescale(value):
    return value * scale

screen = pygame.display.set_mode((output_size[0], output_size[1]))
pygame.display.set_caption('Falling Sand')
clock = pygame.time.Clock()

def hsla_to_rgb(h, s = 100, l = 50, a = 100):
    h /= 360.0
    s /= 100.0
    l /= 100.0

    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return int(r * 255), int(g * 255), int(b * 255), int(a / 100.0 * 255)

def renderDrawWindow():
    #screen.fill((107,222,255))
    screen.fill((0,0,0))
    for y in range(matriz_areia.shape[0]):
        for x in range(matriz_areia.shape[1]):
            if matriz_areia[y, x] == 1:
                pygame.draw.rect(screen, hsla_to_rgb(matriz_cor[y, x]), (rescale(x), rescale(y), rescale(1), rescale(1)))
    pygame.display.update()

def drop_sand():
    global screen
    global frame_count
    global hue_count
    frame_count = frame_count + 1
    if frame_count == 2:
        frame_count = 0
        mouseX, mouseY = pygame.mouse.get_pos()
        index_x = (mouseX//scale)
        index_y = (mouseY//scale)
        if index_x >= 0 and index_x < original_size[0]:
            if index_y >= 0 and index_y < original_size[1]:
                if matriz_areia[index_y, index_x] == 0:
                    matriz_areia[index_y, index_x] = 1
                    matriz_cor[index_y, index_x] = hue_count
                    hue_count = (hue_count + 2) % 360

def falling_grains():
    for y in range(matriz_areia.shape[0]):
        inverted_y = original_size[1] - (y + 1)
        for x in range(matriz_areia.shape[1]):
            if matriz_areia[inverted_y, x] == 1:
                if (inverted_y + 1) < (original_size[1]):
                    new_x = -1
                    if(matriz_areia[inverted_y + 1, x] == 0):
                        new_x = x
                    elif(x - 1 >= 0) and (x + 1 < original_size[0]) and matriz_areia[inverted_y + 1, x - 1] == matriz_areia[inverted_y + 1, x + 1] == 0:
                            choices = [x - 1, x + 1]
                            new_x = random.choice(choices)
                    elif (x - 1 >= 0) and matriz_areia[inverted_y + 1, x - 1] == 0:
                        new_x = x - 1
                    elif (x + 1 < original_size[0]) and matriz_areia[inverted_y + 1, x + 1] == 0:
                        new_x = x + 1

                    if new_x > -1:
                        matriz_areia[inverted_y + 1, new_x] = 1
                        matriz_cor[inverted_y + 1, new_x] = matriz_cor[inverted_y, x]
                        matriz_areia[inverted_y, x] = 0
                        matriz_cor[inverted_y, x] = 0
                

openedScreen = True

while openedScreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            openedScreen = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_pressed = False
        
        if button_pressed == True:
            drop_sand() 

    renderDrawWindow()
    falling_grains()
    clock.tick(60)

pygame.quit()
sys.exit()