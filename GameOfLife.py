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

@jit(nopython=True)
def next_cell(grid, x, y):
    if aliveNeighbours(grid,x,y) == 3:
        return True
    if aliveNeighbours(grid,x,y) == 2:
        return grid[x,y]
    return False

@jit(nopython=True)
def next_grid(grid):
    newGrid = empty_like(grid).astype('bool')
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            newGrid[row,column] = next_cell(grid, row, column)
    return newGrid

# @jit(nopython=True,parallel=True)
def detect_stable_pattern(grid, evolution, i, period=10, verbose = False):
    stable_pattern = False
    for j in range(min(i,period)):
            if (grid == evolution[i-j]).all():
                stable_pattern = True
                if j==0 and verbose: print("\nStable point reached")
                if j!=0 and verbose: print(f"Periodic stable point reached with period {j}")
                break
    return stable_pattern

# @jit(nopython=True)
def start_gol(grid = random.choice(a=[False, True], size=(10, 10), p=[0.5, 0.5]), steps = 100, verbose = False):
    grid.astype('bool')
    evolution = List()
    evolution.append(grid)
    for i in range(Steps-1):
        if verbose and i%10 == 0: print(f"Running Game of Life... Step: {i} / {Steps}", end='\r')
        
        newGrid = next_grid(grid)
        evolution.append(newGrid)
        if detect_stable_pattern(newGrid,evolution,i,verbose=True): break
        
        grid = newGrid
    print("Running Game of Life... Done.")
    return evolution


if __name__ == "__main__":
    #clearConsole()

    fig, ax = plt.subplots()

    GridSize = 501
    Steps = 1000

    InitialGrid = random.choice(a=[False, True], size=(GridSize, GridSize), p=[0.5, 0.5])
    grid = InitialGrid
    ims = []
    loading = ["/","-","\\","|"]

    start = time.time()
    evolution = array(start_gol(grid, Steps, verbose = True),dtype=bool)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))

    # __________________________________________________
    # Analysis

    vitality = zeros([GridSize,GridSize])
    generations = zeros([GridSize,GridSize])
    evolution_int = evolution.astype('int')
    for i,v in enumerate(evolution_int):
        vitality += v
        if i > 0: generations += abs(evolution_int[i] - evolution_int[i-1])

    x = arange(GridSize)
    y = arange(GridSize)
    plt.figure()
    plt.pcolor(x,y,vitality, shading='auto', cmap="CMRmap")
    plt.colorbar(label='Total living time of cell')
    plt.title("Vitality")

    plt.figure()
    plt.pcolor(x,y,generations, shading='auto', cmap="CMRmap")
    plt.colorbar(label='Number of state changes')
    plt.title("Generations")
    plt.show()


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
        if i%10 == 0 : print(f"Saving... Step: {i} / {l}", end="\r")
        savetxt(f"results/simulation_{simulationNumber}/GridEvolution/{i}.numpy", frame, fmt="%i")
    
    print(f"Saving... Done.")


    print("Done.\nGenerating animation...")
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    ani.save(f"results/simulation_{simulationNumber}/evolution.mp4")
    print("Done.")
    plt.show()