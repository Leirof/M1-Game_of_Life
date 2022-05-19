from numpy import *
from numba import jit
import os
import re

# finited borderless space
@jit(nopython=True)
def top(grid, y):    return (y + 1) % len(grid)
@jit(nopython=True)
def bottom(grid, y): return (y - 1) % len(grid)
@jit(nopython=True)
def right(grid, x):  return (x + 1) % len(grid)
@jit(nopython=True)
def left(grid, x):   return (x - 1) % len(grid)

@jit(nopython=True)
def aliveNeighbours(grid,x,y):
    return \
        grid[left(grid,x),top(grid,y)]    + grid[x,top(grid,y)]     + grid[right(grid,x),top(grid,y)]    + \
        grid[left(grid,x),y]              + 0                       + grid[right(grid,x),y]              + \
        grid[left(grid,x),bottom(grid,y)] + grid[x,bottom(grid,y)]  + grid[right(grid,x),bottom(grid,y)]

@jit(nopython=True)
def grid_to_int(grid):
    N,M = grid.shape
    grid = grid.reshape(N*M)
    b = arange(N*M)
    b = flip(b)
    return sum(grid * 2**b)

# def grid_to_hex(grid): return hex(grid_to_int(grid))[2:]
def grid_to_hex(grid, grid_shape=None):
    hxVl = {
    (0, 0, 0, 0): "0",
    (0, 0, 0, 1): "1",
    (0, 0, 1, 0): "2",
    (0, 0, 1, 1): "3",
    (0, 1, 0, 0): "4",
    (0, 1, 0, 1): "5",
    (0, 1, 1, 0): "6",
    (0, 1, 1, 1): "7",
    (1, 0, 0, 0): "8",
    (1, 0, 0, 1): "9",
    (1, 0, 1, 0): "a",
    (1, 0, 1, 1): "b",
    (1, 1, 0, 0): "c",
    (1, 1, 0, 1): "d",
    (1, 1, 1, 0): "e",
    (1, 1, 1, 1): "f"}
    if grid_shape is None: grid_shape = grid.shape
    r=""
    for sL in zip(*(iter(grid.reshape(grid_shape[0]*grid_shape[1])),)*4): r+=hxVl[tuple(sL)]
    return r

def int_to_grid(i, grid_shape):
    print("Int =",i)
    res = zeros(grid_shape[0]*grid_shape[1]).astype(bool)
    print("Bin =",len(bin(i)))
    print("Len(res) =",len(res))
    b = array(list(bin(i))[2:]).astype(bool)
    print("Len(bin) =",len(b))
    res[-len(b):] = b
    return res.reshape(grid_shape)

def hex_to_grid(hexa, grid_shape): return int_to_grid(int(hexa,16), grid_shape)

def grid_to_name(grid):
    N,M = grid.shape
    number = grid_to_hex(grid)
    number = compact_hexa(number)
    return f"{N}x{M}_{number}"

def name_to_grid(name):
    tmp = name.split("_")
    shape = tmp[0].split("x")
    print("Hexa =",tmp[1])
    return hex_to_grid(tmp[1],[int(shape[0]),int(shape[1])])

def save_evolution(file, evolution):
    dir = os.path.split(file)[0]
    if not os.path.isdir(dir): os.makedirs(dir)

    L,N,M = shape(evolution)
    with open(file, "a") as f:
        f.write(f"# Evolution of a {N}*{M} matrix over {L} steps."+"\n")
        f.write(f"# Step\tGrid flattened in hexadecimal"+"\n")
        for i, frame in enumerate(evolution):
            if i%10 == 0 : print(f"📀 Saving results... Step: {i} / {L} ({round(i/L*100)} %)", end="\r")
            f.write(f"{str(i)}\t{grid_to_name(frame).split('_')[1]}\n")

@jit(nopython=True)
def compact_hexa(hexa):
    for _ in range(len(hexa)):
        if hexa[0] == "0": hexa = hexa[1:]
        else: break
    copy = hexa
    cpt = 0
    i=0
    while i < len(hexa):
        if hexa[i] == "0":
            cpt += 1
        else:
            if cpt > 3:
                hexa = hexa[:i-cpt] + f"[{cpt}]" + hexa[i:]
                i = i - cpt + len(f"[{cpt}]")
            cpt = 0
        i += 1
    if cpt > 2:
        hexa = hexa[:i-cpt] + f"[{cpt}]"
    return hexa

@jit(nopython=True)
def uncompact_hexa(hexa):
    res = ""
    i=0
    while i< len(hexa):
        tmp = ""
        c = hexa[i]
        if c == "[":
            j = 1
            while hexa[i+j] != "]":
                tmp += hexa[i+j]
                j+=1
            res += "0"*int(tmp)
            i = i + j
        else:
            res += c
        i+=1
    return res


if __name__ == "__main__":
    a = grid_to_name(array([[0,0,0],[0,1,1],[1,0,0]]))
    print(a)
    print(name_to_grid(a).astype(int))