import json


class HtmlScraper:
    def __get_default_windows_browser(self):
        """Detect the default browser on Windows system"""
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice",
            ) as key:
                browser_name = winreg.QueryValueEx(key, "ProgId")[0]

            if "Chrome" in browser_name:
                return "chrome"
            elif "Firefox" in browser_name:
                return "firefox"
            elif "MSEdge" in browser_name:
                return "edge"
            else:
                return "chrome"  # Default to Chrome if detection fails
        except Exception:
            return "chrome"  # Default to Chrome on error

    def __get_chrome_profile_path(self):
        """Get the default Chrome user profile path on Windows."""
        import os

        local_app_data = os.environ.get("LOCALAPPDATA")
        if not local_app_data:
            return None
        # Default profile is 'Default', but user may have others
        return os.path.join(local_app_data, "Google", "Chrome", "User Data")

    def __load_js_script(self, script_path):
        """Load JavaScript from a file"""
        try:
            with open(script_path, "r") as file:
                return file.read()
        except Exception as e:
            raise Exception(
                f"Failed to load script from {script_path}, error: {str(e)}"
            )

    def print_chrome_profiles_info(self):
        """Print username and email for each Chrome profile."""
        import os

        chrome_profile_path = self.__get_chrome_profile_path()
        if not chrome_profile_path or not os.path.exists(chrome_profile_path):
            print("Chrome profile path not found.")
            return

        profiles = [
            name
            for name in os.listdir(chrome_profile_path)
            if os.path.isdir(os.path.join(chrome_profile_path, name))
            and (name.startswith("Profile") or name == "Default")
        ]

        for profile in profiles:
            profile_dir = os.path.join(chrome_profile_path, profile)
            preferences_path = os.path.join(profile_dir, "Preferences")
            if not os.path.exists(preferences_path):
                continue
            try:
                with open(preferences_path, "r", encoding="utf-8") as f:
                    prefs = json.load(f)
                # Try to get email and name from account_info or profile
                email = None
                name = None
                # Check account_info
                account_info = prefs.get("account_info", [])
                if account_info and isinstance(account_info, list):
                    email = account_info[0].get("email")
                    name = account_info[0].get("full_name")
                # Fallback to profile info
                if not email:
                    email = prefs.get("profile", {}).get("user_name")
                if not name:
                    name = prefs.get("profile", {}).get("name")
                print(f"Profile: {profile}")
                print(f"  Name: {name}")
                print(f"  Email: {email}")
            except Exception as e:
                print(f"Could not read profile {profile}: {e}")

    def get_chrome_profiles_info(self):
        """Return a list of dicts with info for each Chrome profile."""
        import os

        chrome_profile_path = self.__get_chrome_profile_path()
        if not chrome_profile_path or not os.path.exists(chrome_profile_path):
            return []

        profiles = [
            name
            for name in os.listdir(chrome_profile_path)
            if os.path.isdir(os.path.join(chrome_profile_path, name))
            and (name.startswith("Profile") or name == "Default")
        ]

        result = []
        for profile in profiles:
            profile_dir = os.path.join(chrome_profile_path, profile)
            preferences_path = os.path.join(profile_dir, "Preferences")
            if not os.path.exists(preferences_path):
                continue
            try:
                with open(preferences_path, "r", encoding="utf-8") as f:
                    prefs = json.load(f)
                info = {
                    "profile": profile,
                    "name": None,
                    "email": None,
                    "raw": prefs,
                }
                account_info = prefs.get("account_info", [])
                if account_info and isinstance(account_info, list):
                    info["email"] = account_info[0].get("email")
                    info["name"] = account_info[0].get("full_name")
                if not info["email"]:
                    info["email"] = prefs.get("profile", {}).get("user_name")
                if not info["name"]:
                    info["name"] = prefs.get("profile", {}).get("name")
                result.append(info)
            except Exception:
                continue
        return result

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
        browser_type = self.__get_default_windows_browser()

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
