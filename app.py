import webview
from scraper import URLCollector

class ScraperAPI:
    def start_scraping(self, url, pages):
        # Create a new URLCollector instance and run the scraper
        collector = URLCollector()
        collected_urls = collector.run_scraper(url, pages)
        return collected_urls

def start_gui():
    api = ScraperAPI()  # Initialize the API
    window = webview.create_window("PJ Scraper", "index.html", js_api=api)  # Pass the API using js_api
    webview.start()

if __name__ == "__main__":
    start_gui()
