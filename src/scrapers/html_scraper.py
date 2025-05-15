class HtmlScraper:
    def __get_default_windows_browser(self):
        """Detect the default browser on Windows system"""
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
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
    
    def __load_js_script(self, script_path):
        """Load JavaScript from a file"""
        try:
            with open(script_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Failed to load script from {script_path}, error: {str(e)}")
    
    def scrape(self, url):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        import time
        import os
        
        driver = None
        try:
            # Detect default browser
            browser_type = self.__get_default_windows_browser()
            
            # Initialize the appropriate WebDriver based on default browser
            if browser_type == "chrome":
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser_type == "firefox":
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif browser_type == "edge":
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            else:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            
            # Navigate to the URL
            driver.get(url)
            
            # Wait for initial page to load
            time.sleep(2)
            
            # Load and execute the revealSolutions.js script
            script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      'revealSolutions.js')
            js_code = self.__load_js_script(script_path)
            driver.execute_script(js_code)
            
            # Wait for the script to finish executing
            # The script has timeouts based on the number of buttons found
            # Let's estimate a reasonable wait time (5 seconds + potential buttons * 300ms)
            time.sleep(5)  # Base wait time
            
            # Get the page source after script execution
            page_source = driver.page_source
            
            return page_source
        except Exception as e:
            raise Exception(f"Failed to fetch data from {url}, error: {str(e)}")
        finally:
            # Make sure to close the browser
            if driver:
                driver.quit()