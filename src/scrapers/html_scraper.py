from .browser_detection import get_default_windows_browser
from .chrome_profiles import (
    get_chrome_profile_path,
    print_chrome_profiles_info,
    get_chrome_profiles_info,
)
from .script_loader import load_js_script


class HtmlScraper:
    def print_chrome_profiles_info(self):
        print_chrome_profiles_info()

    def get_chrome_profiles_info(self):
        return get_chrome_profiles_info()

    def scrape(self, url, detach=False, profile_dir=None):
        """
        Scrape the given URL using Selenium.
        If detach=True, the browser will remain open after scraping.
        profile_dir: Chrome profile directory name (e.g., 'Default', 'Profile 1')
        """
        from selenium import webdriver  # type: ignore
        from selenium.webdriver.chrome.service import Service as ChromeService  # type: ignore
        from selenium.webdriver.chrome.options import Options as ChromeOptions  # type: ignore
        from selenium.webdriver.firefox.service import Service as FirefoxService  # type: ignore
        from selenium.webdriver.edge.service import Service as EdgeService  # type: ignore
        from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
        from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
        from webdriver_manager.microsoft import EdgeChromiumDriverManager  # type: ignore
        import time
        import os
        import sys
        import subprocess

        driver = None
        # Detect default browser
        browser_type = get_default_windows_browser()

        # Check if Chrome is running and warn user
        if browser_type == "chrome":
            try:
                # Use tasklist to check for running chrome.exe processes
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq chrome.exe"],
                    capture_output=True,
                    text=True,
                )
                if "chrome.exe" in result.stdout.lower():
                    print(
                        "[WARNING] Chrome is currently running. "
                        "Please close all Chrome windows before continuing, "
                        "otherwise profile lock errors may occur."
                    )
            except Exception:
                pass

        # Initialize the appropriate WebDriver based on default browser
        if browser_type == "chrome":
            chrome_options = ChromeOptions()
            import tempfile

            temp_profile = tempfile.mkdtemp()
            chrome_options.add_argument(f"--user-data-dir={temp_profile}")
            chrome_options.add_experimental_option("detach", detach)

            try:
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options,
                )
            except Exception as chrome_exc:
                print("[ERROR] Failed to start ChromeDriver:", chrome_exc)
                print("Tips:")
                print("- Ensure all Chrome windows are closed.")
                print("- Make sure ChromeDriver version matches your installed Chrome.")
                print("- Try updating both Chrome and ChromeDriver.")
                raise
        elif browser_type == "firefox":
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        elif browser_type == "edge":
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install())
            )
        else:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )

        # Navigate to the URL
        driver.get(url)

        # Wait for initial page to load
        time.sleep(5)

        # Return the page source as HTML content
        return driver.page_source
