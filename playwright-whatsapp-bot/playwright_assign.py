from playwright.sync_api import sync_playwright
import pandas as pd
import json
import random
import time
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

contacts = pd.read_excel("contacts.xlsx")

report = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://web.whatsapp.com")

    print("Please scan QR code...")

    # No need to press Enter. Bot waits until WhatsApp opens.
    page.wait_for_selector("div[contenteditable='true']", timeout=120000)

    print("WhatsApp login successful")

    for _, row in contacts.iterrows():

        name = str(row["Name"])
        phone = str(row["Phone"]).replace(".0", "").replace("+", "").strip()
        message = str(row["Message"])

        # Add India country code automatically
        if not phone.startswith("91"):
            phone = "91" + phone

        final_message = message.replace("{name}", name)

        try:
            page.goto(f"https://web.whatsapp.com/send?phone={phone}&text={final_message}")

            page.wait_for_timeout(10000)

            page.wait_for_selector("span[data-icon='send']", timeout=20000)
            page.locator("span[data-icon='send']").click()

            page.wait_for_timeout(5000)

            screenshot_name = f"{name}_{today}.png"
            page.screenshot(path=screenshot_name, full_page=True)

            msgs = page.locator("span.selectable-text")
            total = msgs.count()

            last_messages = []

            for i in range(max(0, total - 3), total):
                last_messages.append(msgs.nth(i).inner_text())

            report.append({
                "Name": name,
                "Phone": phone,
                "Message": final_message,
                "Status": "Sent",
                "Screenshot": screenshot_name,
                "Last3Messages": " | ".join(last_messages)
            })

            print(f"Message sent to {name}")

        except Exception as e:
            report.append({
                "Name": name,
                "Phone": phone,
                "Message": final_message,
                "Status": "Failed",
                "Error": str(e)
            })

            print(f"Failed for {name}")
            print("Error:", e)

        time.sleep(random.randint(2, 5))

    browser.close()

with open(f"whatsapp_report_{today}.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4, ensure_ascii=False)

pd.DataFrame(report).to_excel(f"whatsapp_report_{today}.xlsx", index=False)

print("Report saved")