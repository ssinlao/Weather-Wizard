# Weather Wizard App
This app opens the computer camera and changes the weather based on a single hand gesture by using computer vision.  
**When the camera opens, change the weather by pointing up one finger, two fingers, or three fingers on one hand!**

## Tutorial

To make this project actually work, I migrated to the new MediaPipe version and followed directions in the docs:
<https://developers.google.com/edge/mediapipe/solutions/guide>

Tutorial Video:
[![Build an AMAZING Computer Vision Project in 11 Minutes!](https://youtu.be/_aPM2zzQWmE?si=fK3HphRmSSFDqTLd)](https://youtu.be/_aPM2zzQWmE?si=fK3HphRmSSFDqTLd)

Note: The video tutorial I followed is a bit outdated so it took me a lot more than 11 minutes.

## How to Setup

For this project you need the hand landmarker model from Google which can be downloaded here:
<https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker>

Tip: Scroll to Models section and download "HandLandmarker (full)"
![alt text](<Screenshot 2026-10-14 144911.png>)

Note: I just used VSCode for this project so I made a new virtual environment with ```Ctrl + Shift + P``` and clicked ```> Python:Create Environment```

If needed, install setuptools  
```$ pip install setuptools```

Setup environment using this command (and it will make a .egg-info folder)  
```$ pip install -e .```  

Run project with  
```$ python -m weather_wizard main```  
