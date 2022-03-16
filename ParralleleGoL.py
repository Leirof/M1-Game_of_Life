from numpy import *
from os import cpu_count

cpuCount = 0

def CPUcount():
    global cpuCount
    if not cpuCount : cpuCount = cpu_count()
    return cpuCount

def subGrid(grid, x1,y1,x2,y2):
    sizeX,sizeY = grid.shape
    
    if x1 == -1 :
        grid = roll(grid, 1, axis=0)
        x1 += 1
        x2 += 1
    if x2 == sizeX+1 :
        grid = roll(grid, -1, axis=0)
        x1 -= 1
        x2 -= 1
    if y1 == -1 :
        grid = roll(grid, 1, axis=1)
        y1 += 1
        y2 += 1
    if y2 == sizeX+1 :
        grid = roll(grid, -1, axis=1)
        y1 -= 1
        y2 -= 1

    print(x1,x2,y1,y2)
    return grid[x1:x2,y1:y2]


CPUcount()
print(f"Number of cores: {cpuCount}")

smallestCellSize = 6

grid = loadtxt("structure/u.npy")
GridSize = 20
grid = random.choice(a=[False, True], size=(GridSize, GridSize), p=[0.5, 0.5])

sizeX,sizeY = grid.shape

xSections = sizeX//smallestCellSize
ySections = sizeX//smallestCellSize
smallestCellsCount = xSections * ySections

parrallelCellsCount = min(cpuCount,smallestCellsCount)

print(parrallelCellsCount)
bulk = []
for i in range(parrallelCellsCount):
    bulk.append(None)
print(bulk)

# j=0
# while j < smallestCellsCount:
#     for i in parrallelCellsCount:
#         parrallelCellsCount



