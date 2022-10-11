#NOTE: This will currently NOT work if you start the program while in queue. You must be logged in to the game start the program. I will try to update this.
import time
import datetime
import keyboard
import random
import numpy as np
from scipy.signal import convolve2d
from scipy.signal import savgol_filter
from PIL import ImageGrab
from tkinter import *
from PIL import Image as im


root = Tk()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

left = int(.3*monitor_width)
upper = int(.91*monitor_height)
right = int(.7*monitor_width)
lower = int(.98*monitor_height)
print("Envoy running. You may now live your life.")
run_count = 0

while(True):
    run_count += 1
    sleep_time = random.randrange(10, 15)
    time.sleep(sleep_time)
    screen = ImageGrab.grab(bbox=(left, upper, right, lower), all_screens=False)
    #screen.show()
    matrix = np.asarray(screen)

    bm = matrix.copy()
    for ij in np.ndindex(bm.shape[:2]):
        # Find the scalar magnitude of the current pixel from yellow.
        bmag = np.sqrt((bm[ij][0] - 255)**2 + (bm[ij][1] - 199)**2 + (bm[ij][2])**2)
        # Normalize the magnitude so that values of 0 go to black, and values of 412 (the maximum magnitude) go to white.
        color = ((412-bmag)/412)*255
        if color < 220:
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
    #for i in range(len(values)):
        #for j in range(len(func[i])):
            #func[i][j] = G[values[i], j]

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
        if peaks[p] - peaks[p-1] < 3:
            rm_peaks.append(peaks[p])

    for peak in rm_peaks:
        peaks.remove(peak)

    rm_peaks = []
    for peak in peaks:
        if peak < .1*(lower-upper):
            rm_peaks.append(peak)
            
    for peak in rm_peaks:
        peaks.remove(peak)

    mleft = right-left
    mright = 0
    mtop = lower-upper
    mbot = 0

    for ij in np.ndindex(bm.shape[:2]):
        if bm[ij][0] == 255:
            if ij[1] < mleft:
                mleft = ij[1]
            if ij[1] > mright:
                mright = ij[1]
            if ij[0] < mtop:
                mtop = ij[0]
            if ij[0] > mbot:
                mbot = ij[0]

    #print((mright-mleft)/(mbot-mtop))
    #print("image width:", right-left, "image height:", lower-upper)
    #print("left:", mleft, "right:", mright, "top:", mtop, "bot:", mbot)
    
    
    if 33 <= (mright-mleft)/(mbot-mtop) <= 41:
        #if 0.10 <= (peaks[1]-peaks[0])/len(yhat1) <= 0.14 and 0.33 <= (peaks[2]-peaks[0])/len(yhat1) <= 0.37:
        print(f"Logged out at {datetime.datetime.now()}. Reconnecting...")
        time.sleep(random.randrange(3, 5))
        keyboard.press_and_release('enter')
        time.sleep(random.randrange(15, 20))
        keyboard.press_and_release('enter')
        time.sleep(random.randrange(15, 20))
        keyboard.press_and_release('enter')
        print("Entering world.")
    
