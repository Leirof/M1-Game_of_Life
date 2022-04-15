from numpy import *

# finited borderless space
def top   (int[:,:] grid, int y): return (y + 1) % len(grid)
def bottom(int[:,:] grid, int y): return (y - 1) % len(grid)
def right (int[:,:] grid, int x): return (x + 1) % len(grid)
def left  (int[:,:] grid, int x): return (x - 1) % len(grid)

def aliveNeighbours(int[:,:] grid, int x, int y):
    return \
        grid[left(grid,x),top(grid,y)]    + grid[x,top(grid,y)]     + grid[right(grid,x),top(grid,y)]    + \
        grid[left(grid,x),y]              + 0                       + grid[right(grid,x),y]              + \
        grid[left(grid,x),bottom(grid,y)] + grid[x,bottom(grid,y)]  + grid[right(grid,x),bottom(grid,y)]

def grid_to_int(int[:,:] grid):
    cdef int N,M
    N = len(grid)
    M = len(grid[0])
    cdef int[:,:] b, newGrid
    newGrid = grid.reshape(N*M)
    b = arange(N*M)
    b = flip(b)
    for i,row in enumerate(b):
        for j, element in enumerate(row):
            b[i,j] = grid[i,j] * 2**element
    return sum(b)

def int_to_grid(int i,int N,int M=-1):
    if M is -1: M = N
    return array(list(binary_repr(i).zfill(N*M))).astype(int).reshape([N,M])

def grid_to_name(int[:,:] grid):
    cdef int N, M, number
    N = len(grid)
    M = len(grid[0])
    number = grid_to_int(grid)
    return f"{N}x{M}_{number}"

def name_to_grid(char *name):
    cdef list tmp
    cdef int number, N, M
    tmp = name.split("_")
    number = int(tmp[1])
    tmp = tmp[0].split("x")
    N = int(tmp[0])
    M = int(tmp[1])
    return int_to_grid(number,N,M)