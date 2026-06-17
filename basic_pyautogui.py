import pyautogui
import time

time.sleep(5)  # Switch to Notepad

pyautogui.write('Hello Sakthidasan!', interval=0.1)
pyautogui.press('enter')
pyautogui.write('This text is typed by PyAutoGUI.')