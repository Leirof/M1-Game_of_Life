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
                if j==0 and verbose: print("\n   -> Stable point reached")
                if j!=0 and verbose: print(f"\n   -> Periodic stable point reached with period {j}")
                break
    return stable_pattern

# @jit(nopython=True)
def start_gol(grid = random.choice(a=[False, True], size=(10, 10), p=[0.5, 0.5]), steps = 100, verbose = False):
    grid.astype('bool')
    evolution = List()
    evolution.append(grid)
    for i in range(steps-1):
        if verbose and i%10 == 0: print(f"👾 Running Game of Life... Step: {i} / {steps} ({i/steps*100:.0f} %)", end='\r')
        
        newGrid = next_grid(grid)
        evolution.append(newGrid)
        if detect_stable_pattern(newGrid,evolution,i,verbose=True): return evolution
        
        grid = newGrid
    print(f"👾 Running Game of Life... Step: {steps}/{steps} (100 %) ✅")
    return evolution


if __name__ == "__main__":

    #clearConsole()
     
    print(f"\n👾 Starting Game of Life...",end='\r')

    fig, ax = plt.subplots()

    GridSize = 51
    Steps = 1000

    InitialGrid = random.choice(a=[False, True], size=(GridSize, GridSize), p=[0.5, 0.5])
    grid = InitialGrid
    ims = []
    loading = ["/","-","\\","|"]

    start = time.time()
    evolution = array(start_gol(grid, Steps, verbose = True),dtype=bool)
    end = time.time()
    print("\n⌚ Elapsed (with compilation) = %s s" % round((end - start),2))

    # __________________________________________________
    # Analysis

    print("\n🔎 Analyzing...", end='\r')

    vitality = zeros([GridSize,GridSize])
    generations = zeros([GridSize,GridSize])
    evolution_int = evolution.astype('int')
    for i,v in enumerate(evolution_int):
        if i%10 == 0 : print(f"🔎 Analyzing... Step: {i} / {Steps} ({i/Steps*100:.0f} %)", end='\r')
        vitality += v
        if i > 0: generations += abs(evolution_int[i] - evolution_int[i-1])

    x = arange(GridSize)
    y = arange(GridSize)
    plt.figure(figsize=(10,10))
    plt.subplot(1,2,1)
    plt.pcolor(x,y,vitality, shading='auto', cmap="CMRmap")
    plt.colorbar(label='Total living time of cell')
    plt.title("Vitality")

    plt.subplot(1,2,2)
    plt.pcolor(x,y,generations, shading='auto', cmap="CMRmap")
    plt.colorbar(label='Number of state changes')
    plt.title("Generations")

    print(f"🔎 Analyzing... Step: {Steps}/{Steps} (100 %) ✅")

    # __________________________________________________
    # Saving results

    print("\n📀 Saving results...", end="\r")

    simulationNumber = 0

    if not os.path.isdir("results"): os.makedirs("results")

    # Determining the number (identifier) of the simulation
    if os.path.isfile("results/manifest.dat"):
        for line in open("results/manifest.dat", "r"):
            simulationNumber = int(line) + 1
            break
    with open("results/manifest.dat", "w+") as f:
        f.write(str(simulationNumber))
            
    os.makedirs(f"results/simulation_{simulationNumber}/GridEvolution")

    """
    savetxt(f"results/simulation_{simulationNumber}/InitialGrid.numpy", grid, fmt="%i")
    savetxt(f"results/simulation_{simulationNumber}/SimulationProperties.numpy", evolution.shape)
    """

    file = f"results/simulation_{simulationNumber}/GridEvolution.txt"

    save_evolution(file, evolution)
    
    print(f"📀  Saving results... Step: {len(evolution)}/{len(evolution)} (100 %) ✅\n   -> Saved in {file}")


    print("\n🎞️ Generating animation...", end="\r")
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    ani.save(f"results/simulation_{simulationNumber}/evolution.mp4")
    print("🎞️ Generating animation... ✅")
    print(" ")
    plt.show()