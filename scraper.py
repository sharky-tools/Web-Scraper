# scraper.py

import time
import random
import logging
import base64
import os
import stat
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('url_collector.log'),
        logging.StreamHandler()
    ]
)

class Config:
    BASE_URL = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=btp&ou=ile-de-france&univers=pagesjaunes&idOu="
    DELAY_MIN = 2
    DELAY_MAX = 4

class URLCollector:
    def __init__(self, output_file='file.txt'):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        # Get path to driver using webdriver_manager
        driver_path = ChromeDriverManager().install()

        # 🐧 Linux Fix: Ensure chromedriver is executable
        if platform.system() == 'Linux':
            os.chmod(driver_path, os.stat(driver_path).st_mode | stat.S_IEXEC)

        self.driver = webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options
        )

    def random_delay(self):
        time.sleep(random.uniform(Config.DELAY_MIN, Config.DELAY_MAX))

    def accept_cookies(self):
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            cookie_button.click()
            logging.info("Cookies accepted")
            self.random_delay()
        except Exception as e:
            logging.warning(f"Cookie acceptance failed: {e}")

    def collect_urls_from_page(self):
        try:
            companies = self.driver.find_elements(
                By.CSS_SELECTOR, "div.bi-content div.bi-header-title a.bi-denomination"
            )
            
            page_urls = []
            for company in companies:
                href = company.get_attribute('href')
                if href:
                    if href.startswith('/pros/'):
                        full_url = f"https://www.pagesjaunes.fr{href}"
                    elif href.startswith('#'):
                        data_pjlb = company.get_attribute('data-pjlb')
                        if data_pjlb:
                            decoded_path = base64.b64decode(data_pjlb.split('"url":"')[1].split('"')[0]).decode('utf-8')
                            full_url = f"https://www.pagesjaunes.fr{decoded_path}"
                        else:
                            continue
                    else:
                        full_url = href
                    
                    page_urls.append(full_url)
            
            return page_urls
        except Exception as e:
            logging.error(f"Error collecting URLs: {e}")
            return []

    def save_urls(self, urls):
        with open(self.output_file, 'a', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        logging.info(f"Saved {len(urls)} URLs to {self.output_file}")

    def run_scraper(self, url, pages):
        self.driver.get(url)
        self.random_delay()
        self.accept_cookies()

        collected_urls = []
        page_number = 1
        while page_number <= pages:
            logging.info(f"Processing page {page_number}")
            
            # Collect URLs from current page
            current_page_urls = self.collect_urls_from_page()
            collected_urls.extend(current_page_urls)

            # Try to find and click next page button
            try:
                next_page_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "pagination-next"))
                )
                next_page_button.click()
                page_number += 1
                self.random_delay()
            except Exception:
                logging.info("No more pages available")
                break

        # Save the URLs
        self.save_urls(collected_urls)
        return collected_urls
