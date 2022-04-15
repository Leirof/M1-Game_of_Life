from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from GoL_utils import *
import time
from numba import jit
from numba.typed import List


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# @jit(nopython=True)
def next_cell(grid, x, y):
    if aliveNeighbours(grid,x,y) == 3:
        return True
    if aliveNeighbours(grid,x,y) == 2:
        return grid[x,y]
    return False

# @jit(nopython=True)
def next_grid(grid):
    newGrid = empty_like(grid)
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            newGrid[row,column] = next_cell(grid, row, column)
    return newGrid

# @jit(nopython=True,parallel=True)
def detect_stable_pattern(grid, evolution, i, period=1000, verbose = False):
    stable_pattern = False
    for j in range(min(i,period)):
            if (grid == evolution[i-j]).all():
                stable_pattern = True
                if j==0 and verbose: print("Stable point reached")
                if j!=0 and verbose: print(f"Periodic stable point reached with period {j}")
                break
    return stable_pattern

# @jit(nopython=True)
def start_gol(grid = random.choice(a=[False, True], size=(1000, 1000), p=[0.5, 0.5]),steps = 1000, verbose = False):
    grid.astype('int')
    evolution = List()
    evolution.append(grid)
    for i in range(Steps-1):
        if verbose and i%10 == 0: print(f"Running Game of Life... Step: {i} / {Steps}")
        
        newGrid = next_grid(grid)
        evolution.append(newGrid)
        if detect_stable_pattern(newGrid,evolution,i,verbose=True): break
        
        grid = newGrid
    print(f"Running Game of Life... Done.")
    return evolution


if __name__ == "__main__":
    #clearConsole()

    fig, ax = plt.subplots()

    GridSize = 501
    Steps = 1000

    InitialGrid = random.choice(a=[False, True], size=(GridSize, GridSize), p=[0.5, 0.5])
    # InitialGrid = zeros([GridSize,GridSize])
    # structure = loadtxt("structure/u.npy")
    # sizeX, sizeY = structure.shape
    # posX = 23
    # posY = 23
    # InitialGrid[posX:posX+sizeX,posY:posY+sizeY] = structure
    

    # evolution = empty([Steps,GridSize,GridSize])
    # evolution[0] = InitialGrid
    grid = InitialGrid

    # ims is a list of lists, each row is a list of artists to draw in the
    # current frame; here we are just animating one artist, the image, in
    # each frame
    ims = []
    loading = ["/","-","\\","|"]

    start = time.time()
    evolution = array(start_gol(grid, Steps, verbose = True),dtype=bool)
    # for i in range(Steps-1):
    #     if i%10 == 0:
    #         # clearConsole()
    #         print(f"Computing evolution... Step: {i} / {Steps}", end="\r")
    #     im = ax.imshow(grid, animated=True)
    #     if i == 0:
    #         ax.imshow(grid)  # show an initial one first
    #     ims.append([im])
    #     if sum(grid) == 0:
    #         print("Every cells was destroyed")
    #         break
    #     newGrid = next_grid(grid)
    #     if (newGrid == grid).all():
    #         print("Stable point reached")
    #         break
    #     grid = newGrid
    #     evolution[i+1] = grid
    # print(f"Computing evolution... Done.")
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))

    # __________________________________________________
    # Saving results

    print("Done.\nSaving Results...")

    simulationNumber = 0

    if not os.path.isdir("results"): os.makedirs("results")

    if os.path.isfile("results/manifest.dat"):
        for line in open("results/manifest.dat", "r"):
            simulationNumber = int(line) + 1
            break

    with open("results/manifest.dat", "w+") as f:
            f.write(str(simulationNumber))

    os.makedirs(f"results/simulation_{simulationNumber}/GridEvolution")
    savetxt(f"results/simulation_{simulationNumber}/InitialGrid.numpy", grid, fmt="%i")
    savetxt(f"results/simulation_{simulationNumber}/SimulationProperties.numpy", evolution.shape)
    
    l = len(evolution)
    for i, frame in enumerate(evolution):
        if i%10 == 0 : print(f"Saving... Step: {i} / {l}")
        savetxt(f"results/simulation_{simulationNumber}/GridEvolution/{i}.numpy", frame, fmt="%i")
    
    print(f"Saving... Done.")


    print("Done.\nGenerating animation...")
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    ani.save(f"results/simulation_{simulationNumber}/evolution.mp4")
    print("Done.")
    plt.show()