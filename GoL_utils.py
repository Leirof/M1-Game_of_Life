from numpy import *
from numba import jit

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

@jit(nopython=True,parallel=True)
def grid_to_int(grid):
    N,M = grid.shape
    grid = grid.reshape(N*M)
    b = arange(N*M)
    b = flip(b)
    return sum(grid * 2**b)

@jit(nopython=True,parallel=True)
def int_to_grid(i,N,M=None):
    if M is None: M = N
    return array(list(binary_repr(i).zfill(N*M))).astype(int).reshape([N,M])

@jit(nopython=True,parallel=True)
def grid_to_name(grid):
    N,M = grid.shape
    number = grid_to_int(grid)
    return f"{N}x{M}_{number}"

@jit(nopython=True,parallel=True)
def name_to_grid(name):
    tmp = name.split("_")
    number = int(tmp[1])
    tmp = tmp[0].split("x")
    N = int(tmp[0])
    M = int(tmp[1])
    return int_to_grid(number,N,M)