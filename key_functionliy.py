from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. Open AccuWeather site
    page.goto("https://www.accuweather.com/en/in/bodinayakkanur/190774/10-day-weather-forecast/190774")

    # 2. Wait page load
    page.wait_for_timeout(5000)

    # 3. Click Hourly
    page.click("text=Hourly")

    # 4. Wait after click
    page.wait_for_timeout(5000)

    # 5. Take screenshot
    page.screenshot(path="bodinayakkanur_hourly_weather.png", full_page=True)

    print("Hourly weather page opened and screenshot saved.")

    browser.close()