# Weather Wizard App
This app opens the computer camera and changes the weather based on what hand gesture is read with computer vision.

## Tutorial

To make this project actually work, I migrated to the new MediaPipe version and followed directions in the docs:
<https://developers.google.com/edge/mediapipe/solutions/guide>

Tutorial Video:
<iframe width="560" height="315" src="https://www.youtube.com/embed/_aPM2zzQWmE?si=W3SPik_i6jDc92wd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

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
