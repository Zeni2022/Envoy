# Envoy

NOTE: Currently Envoy will not work if you run it while in queue. Envoy will think you have been disconnected and attempt to log you in (which will fail). I plan on updating this but for now it is unsupported. Anyone running Envoy on a monitor resolution vastly different from mine (2560x1440) may have issues. If you follow the instructions correctly and still have issues, and your monitor resolution is very different from mine, reach out to me so I can improve Envoy to run on monitors of different resolutions.

## How Envoy Works

Envoy regularly takes screenshots of your screen. An analysis is done on this screenshot to figure out the current status of your connection in-game (a more detailed explanation is at the bottom of this README if you're interested). When fully disconnected (i.e. the screen with ICC in the background and the frost dragon) it will reconnect you to the character select screen, then put you in-game. Envoy will NOT play your character or give any inputs to your computer while you are logged into the game. This is ONLY done when you are on the disconnected screen. The motivation behind creating Envoy was that even when we are connected to WoW and online, we have to babysit the game to make sure we don't get kicked out. If you aren't checking remote desktop regularly while at work, walking your dog, at the grocery store, pretending to listen to loved ones, you risk getting disconnected and having to try again tomorrow. Envoy will run while you are away from your PC to ensure you keep yourself logged in and out of queue. If there are confusions, doubts, or issues regarding Envoy please reach out to me.

## Usage Instructions

Ultimately it's simple, but messing up a small detail could result in Envoy not working properly. Envoy does not inject into WoW like other softwares do, making it safer but more delicate. When running Envoy, WoW.exe MUST be your active window. Do not let another app be your currently active window while Envoy is running because it will interact with that window instead of WoW.exe. Make sure that WoW.exe is also on your main monitor. If you have a multiple monitor setup and you don't know which monitor is your main monitor, double-check before running Envoy. If WoW.exe is not on the main monitor Envoy will not be able to take screenshots successfully. Currently, the intended use for Envoy is for you to be connected and logged into WoW, WoW.exe to be full-screened on your main monitor and be the currently active window.

## Step 0: Download Envoy

![image](https://user-images.githubusercontent.com/115406246/194967276-8da3ed4c-eae5-4535-9db5-8c2078f120f4.png)
You can download the project by clicking the Download ZIP button. You will have to unzip this project in a location that you will remember for later. Putting it in downloads is a convenient spot.

## Step 1: Install Python

![image](https://user-images.githubusercontent.com/115406246/194968021-5e9b22bc-52ca-4fd1-83f2-0921aedbf6b0.png)

In order for Envoy to work, you must have Python installed on your computer and a few Python libraries. When installing Python I would recommend using the Microsoft Store (it's free). Just hit the windows key and type "Microsoft Store". Click the first option and type "python". Click "Get" and you should be good to go.

![image](https://user-images.githubusercontent.com/115406246/194968572-98d94211-69d7-4843-9562-30c8e8e2a513.png)

With Python installed, the language Envoy runs off of is now on your PC. The last thing to do is install the proper packages that Envoy uses. These Python modules are widely distributed.

### PowerShell
I'm going to assume most of you are on Windows for now - Open up PowerShell. To do this press the windows key, type "Windows PowerShell" and click the first app that comes up. For me, when I open PowerShell my line says
```
PS C:\Users\{name}>
```
Yours may look differently but follow accordingly, if you have questions reach out to me. We will be typing the next commands directly here. To double check that Python is installed correctly and running, type:
```
PS C:\Users\{name}> python
```

PowerShell should tell you that Python launched with its corresponding version, and all you will see is:
```
>>>
```
If this is the case, python is running correctly. You can type
```
>>>quit()
```
to get out of Python.

![image](https://user-images.githubusercontent.com/115406246/194968847-3142b29c-e42a-4865-aeaf-52daea9eb909.png)

If you are able to follow this with the same output, you're good to go.

## PIP
Python PIP is the package installer for Python modules. It allows us to remotely install packages, which we will need for Envoy to work. PIP comes pre-installed on Python 3.4 and later, so you will have it after installing Python if you chose the above link, or a new version.

### Python modules
Installing all of the required modules can be done with one line in PowerShell:
```
PS C:\Users\{name}> pip install keyboard numpy scipy Pillow tk
```
Keyboard should be successfully installed after doing this.
It should look like this:

![Untitled](https://user-images.githubusercontent.com/115406246/194914147-6d7ccf5e-b005-41df-a359-051c3d7032bd.png)


## Using Envoy
Now Envoy is ready to run. You need to know what directory you put Envoy in. If it went into your downloads, it is most likely in "C:\Users\{name}\Downloads\Envoy-master\envoy-master". But it could be in a different location depending on how you downloaded it. In PowerShell, cd to Envoy. I will include a picture below of what it looks like for me.

![Untitled](https://user-images.githubusercontent.com/115406246/194914470-a402f198-c55e-47b6-80fe-6270e12c5286.png)

As you can see, my Envoy.py file is stored in C:\Users\bucky\downloads\envoy-master\envoy-master. Once I run
```
cd C:\Users\bucky\Downloads\envoy-master\envor-master
```
I am able to run
```
PS C:\Users\bucky\downloads\envoy-master\envoy-master> python Envoy.py
```
Now Envoy is running and regularly taking screenshots of your screen to check your online status.

You may want to re-read the instructions at the top of this README to be sure of the intended use-cases for Envoy. Improper use may result in Envoy not running correctly, and ultimately not keeping you logged in.

## Terminating Envoy
When you want to end Envoy, simply click on PowerShell so that it's your current window (the same window that you ran Envoy with) and press Ctrl-C. Ctrl-C is a keyboard interrupt for python scripts, and will end the process. You will have to run the same "python Envoy.py" command afterwards if you want to run it at a later time.

![image](https://user-images.githubusercontent.com/115406246/194777305-5e452aee-c56d-4cb4-93e5-eda4d79cadef.png)



### Detailed explanation of how Envoy works:
A [sobel operator](https://en.wikipedia.org/wiki/Sobel_operator) is applied to the images for edge-detection with a custom kernel based off of the colors Blizzard uses for their log-in screen. A [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter) is applied to a linearly interpolated function mapping pixel locations to their colors after the sobel operator. Once Envoy has detected that you were disconnected from the game based on signatures unique to the login screen, it will reconnect you by pressing enter on your keyboard via the Python keyboard module.
