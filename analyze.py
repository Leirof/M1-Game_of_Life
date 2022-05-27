import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time

def generate_animation(evolution, save_as = None, plot=False, verbose = False):

    if verbose : print("\n🎞️ Generating animation...", end="\r")

    fig = plt.figure()
    i=0
    im = plt.imshow(evolution[0], animated=True)
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")
        im.set_array(evolution[i])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)

    print(f"🎞️ Generating animation... Step: {len(evolution)}/{len(evolution)} (100 %) ✅")

    # __________________________________________________
    # Saving animation

    if save_as: 
        if verbose : print(f"\n📀  Saving animation...", end="\r")
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)
        if verbose : print(f"📀  Saving animation... ✅\n   -> Saved in {save_as}")

    if plot: plt.show()