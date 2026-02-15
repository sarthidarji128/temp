from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import threading
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
page_title = "Initializing..."
last_refresh = "Not started"
refresh_count = 0
monitor_status = "Starting..."

def monitor_github():
    """Background thread to monitor GitHub page"""
    global page_title, last_refresh, refresh_count, monitor_status
    
    logger.info("=== MONITOR THREAD STARTED ===")
    
    try:
        logger.info("Configuring Chrome options...")
        # Chrome options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        logger.info("Starting Chrome with Selenium Manager (auto-downloads correct ChromeDriver)...")
        # Selenium 4.6+ automatically manages ChromeDriver via Selenium Manager
        # No need for webdriver-manager package
        driver = webdriver.Chrome(options=options)
        logger.info("ChromeDriver initialized successfully")

        url = "https://github.com/sarthidarji128"
        logger.info(f"Opening URL: {url}")
        driver.get(url)

        page_title = driver.title
        monitor_status = "Running"
        logger.info(f"✓ Page loaded successfully!")
        logger.info(f"✓ Page Title: {page_title}")
        logger.info(f"✓ Profile visited successfully.")
        logger.info("=== STARTING REFRESH LOOP ===")

        # Refresh page every 5 seconds
        while True:
            time.sleep(5)
            driver.refresh()
            refresh_count += 1
            last_refresh = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"📄 Page refresh #{refresh_count} at {last_refresh}")

    except Exception as e:
        monitor_status = f"Error: {str(e)}"
        logger.error(f"❌ ERROR in monitor thread: {e}", exc_info=True)
    finally:
        try:
            driver.quit()
            logger.info("Browser closed")
        except:
            pass



if __name__ == '__main__':
    logger.info("Selenium monitoring starting...")
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitor_github, daemon=True)
    monitor_thread.start()
    logger.info("Monitor thread started")

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
