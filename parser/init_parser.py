from selenium import webdriver
from selenium_stealth import stealth


# Инициализируем родительский класс Parser
class Parser:

    # Констуктор в котором формируется сессия
    def __init__(self, url: str):
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options, executable_path='parser/chromedriver')

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.url = url
        self.result = []





