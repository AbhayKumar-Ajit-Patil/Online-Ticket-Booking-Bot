from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

class ArsenalTicketBot:
    def __init__(self):
        print("Initializing ArsenalTicketBot...")
        self.driver = None
        self._setup_driver()

    def _setup_driver(self):
        print("Setting up driver...")
        options = Options()

        headless = os.getenv("ARS_HEADLESS", "false").lower() == "true"
        if headless:
            options.add_argument("--headless")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")



        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        print("Driver successfully set up.")

    def open_website(self):
        print("Opening website...")

        fixture_url = os.getenv("ARS_FIXTURE_URL")
        print("Fixture URL from env:", fixture_url)

        if fixture_url and fixture_url.startswith("http"):
            self.driver.get(fixture_url)
            print("Successfully opened:", fixture_url)
            time.sleep(3)
        else:
            raise Exception(" No valid fixture URL provided.")


    def login(self):
        print("Attempting login...")
        email = os.getenv("ARS_EMAIL")
        password = os.getenv("ARS_PASS")
        if not email or not password:
            raise Exception("Email or password not provided.")

        try:
            
            self.driver.find_element(By.ID, "login-email").send_keys(email)
            self.driver.find_element(By.ID, "login-password").send_keys(password)
            self.driver.find_element(By.ID, "login-button").click()
            time.sleep(3)
            print("Login completed.")
        except Exception as e:
            print("Login failed:", e)

    def select_tickets(self):
        print("Selecting tickets...")
        blocks = os.getenv("ARS_BLOCKS", "").split(",")
        prices = os.getenv("ARS_PRICES", "").split(",")
        qty = int(os.getenv("ARS_QTY", "1"))
        print(f"Ticket preferences: {qty} ticket(s), blocks={blocks}, prices={prices}")
        
        time.sleep(2)

    def close(self):
        print("Closing browser...")
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


def run_bot():
    print("Bot starting...")
    bot = ArsenalTicketBot()
    bot.open_website()
    bot.login()
    bot.select_tickets()
    bot.close()
    print("Bot finished.")
