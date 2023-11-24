import pyautogui
import time


time.sleep(1)
print("a")
location = pyautogui.locateOnWindow('icon-fire.png',"Fire | AdventureQuest Wiki",confidence=0.85,limit=10)
#pyautogui.locateon
print("b")
try:
    print(location)
except:
    print("Not found")