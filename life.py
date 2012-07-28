# -*- coding: utf-8 -*-
# jmcgee

import time
import numpy as np
from scipy import ndimage
import pygame
from pygame.locals import *
import timeit

game_dim = (300,300)
disp_dim = (600,600)

dtype = np.int8
depth = 8
max_int = 2**8/2 - 1

kernel = np.ones((3,3), dtype=dtype)
kernel[1,1] = 0

game_state = np.random.binomial(1, 0.6, size=game_dim).astype(dtype)
game_tmp = np.ndarray(game_dim, dtype=dtype)
game_bool1 = np.ndarray(game_dim, dtype=np.bool)
game_bool2 = np.ndarray(game_dim, dtype=np.bool)

def set_r_pentomino(data):
    x, y = game_dim
    x = int(x/2)
    y = int(y/2)
    data[x,y] = 1
    data[x,y-1] = 1
    data[x-1,y] = 1
    data[x+1,y] = 1
    data[x-1,y+1] = 1

def set_glider(data, dim):
    x, y = dim
    x = int(x/2)
    y = int(y/2)
    data[x,y+1] = 1
    data[x-1,y+1] = 1
    data[x+1,y+1] = 1
    data[x+1,y] = 1
    data[x,y-1] = 1

def show_array(data_array, data_surf, disp_surf):
    np.multiply(max_int, data_array, out=game_tmp)
    pygame.surfarray.blit_array(data_surf, game_tmp)
    pygame.transform.scale(data_surf, disp_surf.get_size(), disp_surf)
    pygame.display.update()

def next_step(state):
    neighbors = game_tmp
    ndimage.convolve(state, kernel, output=neighbors)
    np.greater_equal(neighbors, 2, out=game_bool1)
    np.less_equal(neighbors, 3, out=game_bool2)
    np.multiply(game_bool1, game_bool2, out=game_bool1)
    np.multiply(state, game_bool1, out=state)
    np.equal(neighbors, 3, out=game_bool1)
    np.add(state, game_bool1, out=state)
    np.clip(state + game_bool1, 0, 1, out=state)

def handle_events():
    e = pygame.event.poll()
    if e.type == pygame.locals.QUIT: raise SystemExit
    #elif e.type == pygame.locals.KEYDOWN: break

#set_glider(game_state, (8,8))
#set_r_pentomino(game_state)

def main_loop():
    step = 0
    while True:
        show_array(game_state, game_surf, screen_surf)
        next_step(game_state)
        handle_events()
        step += 1
        time.sleep(0.1)

def test():
    global game_state
    next_step(game_state)

def test1():
    global game_state
    next_step1(game_state)

def time_test(f, n):
    t = timeit.Timer(f)
    print t.timeit(int(n))

#time_test(test, 1000)

pygame.init()
screen_surf = pygame.display.set_mode(disp_dim, 0, depth)
game_surf = pygame.Surface(game_dim, 0, depth)

main_loop()