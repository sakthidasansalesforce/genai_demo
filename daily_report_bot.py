import pyautogui
import time
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. Open Chrome
pyautogui.press("win")
time.sleep(1)
pyautogui.write("chrome")
pyautogui.press("enter")
time.sleep(3)

# 2. Open weather site
pyautogui.write("https://www.google.com/search?q=weather+today")
pyautogui.press("enter")
time.sleep(5)

# 3. Copy weather data manually from screen
pyautogui.hotkey("ctrl", "l")
pyautogui.write("weather today")
pyautogui.press("enter")
time.sleep(5)

# Example simple data
weather_data = "Weather checked from Google"
comment = "Good for daily status report"

# 4. Open Excel
pyautogui.press("win")
time.sleep(1)
pyautogui.write("excel")
pyautogui.press("enter")
time.sleep(5)

# Create blank workbook
pyautogui.press("enter")
time.sleep(3)

# Type data in Excel
pyautogui.write("Date and Time")
pyautogui.press("tab")
pyautogui.write("Fetched Data")
pyautogui.press("tab")
pyautogui.write("Comment")

pyautogui.press("enter")
pyautogui.write(now)
pyautogui.press("tab")
pyautogui.write(weather_data)
pyautogui.press("tab")
pyautogui.write(comment)

# 5. Save Excel file
pyautogui.hotkey("ctrl", "s")
time.sleep(2)
pyautogui.write(f"daily_report_{today}.xlsx")
pyautogui.press("enter")
time.sleep(2)

# Take screenshot
screenshot = pyautogui.screenshot()
screenshot.save(f"daily_report_screenshot_{today}.png")