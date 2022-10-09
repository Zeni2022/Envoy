#NOTE: This will currently NOT work if you start the program while in queue. You must be logged in to the game start the program. I will try to update this.
import time
import keyboard
import random
import numpy as np
from scipy.signal import convolve2d
from scipy.signal import savgol_filter
from PIL import ImageGrab
from tkinter import *
# Delete this import
from PIL import Image as im
import matplotlib.pyplot as plt
#

root = Tk()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

left = 0
upper = int(.64*monitor_height)
right = int(.156*monitor_width)
lower = int(.87*monitor_height)
print("Envoy running. You may now live your life.")
run_count = 0

while(True):
    run_count += 1
    sleep_time = random.randrange(10, 15)
    time.sleep(sleep_time)
    screen = ImageGrab.grab(bbox=(left, upper, right, lower), all_screens=False)
    matrix = np.asarray(screen)

    bm = matrix.copy()
    for ij in np.ndindex(bm.shape[:2]):
        # Find the scalar magnitude of the current pixel from blue.
        bmag = np.sqrt((bm[ij][0] - 24)**2 + (bm[ij][1] - 84)**2 + (bm[ij][2] - 139)**2)
        # Normalize the magnitude so that values of 0 go to black, and values of 320 (the maximum magnitude) go to white.
        color = 255 - ((320-bmag)/320)*255
        if color < 180:
            color = 0
        else:
            color = 255
        # Greyscale it.
        bm[ij][0] = color
        bm[ij][1] = color
        bm[ij][2] = color

    #data = im.fromarray(bm)
    #data.show()

    # Kernel generator
    a1 = np.matrix([.33, .66, .33])
    a2 = np.matrix([-.33, 0, .33])
    Kx = a1.T * a2
    Ky = a2.T * a1

    # Apply Sobel operator
    Gx = convolve2d(bm[:,:,0], Kx, "same", "symm")
    Gy = convolve2d(bm[:,:,0], Ky, "same", "symm")
    G = np.sqrt(Gx**2 + Gy**2)

    #data = im.fromarray(G)
    #data.show()

    func_axis = [i for i in range(lower-upper)]
    func = [[0 for i in range(lower-upper)] for j in range(3)]

    values = [int(right/2 - (.125*right)), int(right/2), int(right/2 + (.125*right))]
    for i in range(len(values)):
        for j in range(len(func[i])):
            func[i][j] = G[values[i], j]

    avg_func = func[0]
    for i in range(len(avg_func)):
        avg_func[i] = (func[0][i] + func[1][i] + func[2][i])/3

    yhat1 = savgol_filter(avg_func, 39, 3)

    peaks = []

    for i in range(10, len(yhat1)-10):
        count = 0
        flag = True
        c_val = yhat1[i]
        for j in range(1,10):
            if yhat1[i-j] >= c_val or yhat1[i+j] >= c_val:
                count += 1
                if count > 1:
                    flag = False
                    break
        if flag:
            peaks.append(i)

    #plt.plot(func_axis, avg_func, color='red')
    #plt.plot(func_axis, yhat1, color='blue')
    #plt.show()

    rm_peaks = []
    for p in range(1, len(peaks)):
        if peaks[p] - peaks[p-1] < 2:
            rm_peaks.append(peaks[p])

    for peak in rm_peaks:
        peaks.remove(peak)

    if len(peaks) == 3:
        if 0.10 <= (peaks[1]-peaks[0])/len(yhat1) <= 0.14 and 0.33 <= (peaks[2]-peaks[0])/len(yhat1) <= 0.37:
            print("Logged out. Reconnecting...")
            time.sleep(random.randrange(3, 5))
            keyboard.press_and_release('enter')
            time.sleep(random.randrange(10, 15))
            keyboard.press_and_release('enter')
            time.sleep(random.rangerange(10, 15))
            keyboard.press_and_release('enter')
            print("Logging in...")
    
