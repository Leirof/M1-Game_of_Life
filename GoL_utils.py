from numpy import *
from numba import jit
import os

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

@jit(nopython=True)
def int_to_grid(i,N,M=None):
    if M is None: M = N
    return array(list(binary_repr(i).zfill(N*M))).astype(int).reshape([N,M])

@jit(nopython=True)
def grid_to_name(grid):
    N,M = grid.shape
    number = grid_to_int(grid)
    return f"{N}x{M}_{number}"

@jit(nopython=True)
def name_to_grid(name):
    tmp = name.split("_")
    number = int(tmp[1])
    tmp = tmp[0].split("x")
    N = int(tmp[0])
    M = int(tmp[1])
    return int_to_grid(number,N,M)

@jit(nopython=True)
def grid_to_hex(grid, grid_shape=None):
    if grid_shape is None: grid_shape = grid.shape
    return hex(int("".join(grid.reshape(grid_shape[0]*grid_shape[1]).astype(str))))[2:]

@jit(nopython=True)
def grid_to_hex2(grid, grid_shape=None):
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

def hex_to_grid(hex, grid_shape):
    # TODO
    pass

def save_evolution(file, evolution):
    dir = os.path.split(file)[0]
    if not os.path.isdir(dir): os.makedirs(dir)

    L,N,M = shape(evolution)
    with open(file, "a") as f:
        f.write(f"# Evolution of a {N}*{M} matrix over {L} steps."+"\n")
        for i, frame in enumerate(evolution):
            frame = frame.reshape(N*M)
            if i%10 == 0 : print(f"📀 Saving results... Step: {i} / {L} ({round(i/L*100)} %)", end="\r")
            f.write(array2string(packbits(frame))+"\n")

if __name__ == "__main__":
    print(grid_to_hex2(array([[0,0,0],[0,1,1],[1,0,0]])))
