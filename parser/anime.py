import selenium.common
from parser.init_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


# Класс для парсинга метаданных определенного аниме
class Anime(Parser):

    # Парсим результаты поиска
    def parse_page(self, title: str) -> selenium.webdriver:
        self.driver.get(self.url)

        input = self.driver.find_element(By.CLASS_NAME, "form-control-lg").find_element(By.TAG_NAME, "input")
        input.send_keys(title)
        input.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-county"))
            )
        except selenium.common.TimeoutException:
            return "Неправильное название"

        switch_to = self.driver.find_elements(By.CLASS_NAME, "nav-link")

        for element in switch_to:
            try:
                if element.find_element(By.CLASS_NAME, "text-link-gray").text:
                    element.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "active"))
                    )
                    break
            except selenium.common.exceptions.NoSuchElementException:
                pass

        titles = self.driver.find_elements(By.CLASS_NAME, "animes-grid-item")

        return titles

    # Проверяем есть ли такое аниме
    @staticmethod
    def is_valid_title(title: str, titles: selenium.webdriver) -> str:
        for element in titles:
            if title.lower() == element.find_element(By.CLASS_NAME, "card-title").text.lower():
                return element.find_element(By.CLASS_NAME, "card-title").text

    # Проверяем статус аниме
    def is_valid_status(self, title: str) -> bool:
        titles = self.driver.find_elements(By.CLASS_NAME, "card-title")

        for element in titles:
            if element.text.lower() == title.lower():
                element.find_element(By.LINK_TEXT, element.text).click()
                break

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "anime-info"))
        )

        anime_info = self.driver.find_element(By.CLASS_NAME, "anime-info").find_elements(By.CLASS_NAME, "col-sm-8")

        for attr in anime_info:
            if attr.text == "Онгоинг":
                return True

    # Собираем данные о аниме
    def parse_title(self) -> list:
        attrs = self.driver.find_element(By.CLASS_NAME, "anime-info").find_elements(By.TAG_NAME, "dd")

        anime_title = self.driver.find_element(By.CLASS_NAME, "anime-title").find_element(By.TAG_NAME, 'h1').text

        date_release = self.convert_date(attrs[0])
        result = [anime_title, attrs[5].text, attrs[10].text, date_release]

        return result

    # Преобразуем дату в правильный формат
    @staticmethod
    def convert_date(date_release: selenium.webdriver) -> datetime:
        month = {
            'янв.': '01',
            'фев.': '02',
            'мар.': '03',
            'апр.': '04',
            'мая': '05',
            'июн.': '06',
            'июл.': '07',
            'авг.': '08',
            'сент.': '09',
            'окт.': '10',
            'нояб.': '11',
            'дек.': '12',

        }

        date_release = date_release.text[:date_release.text.find(':') - 5].rstrip().split()

        for key in month:
            if key in date_release:
                date_release[date_release.index(key)] = month.get(key)
                break

        date_release = datetime.datetime.strptime("-".join(date_release), '%d-%m-%Y').date()\
            + datetime.timedelta(days=1)

        return date_release

    # Собираем все воедино
    def run(self, title: str) -> list or str:
        # Получаем результаты запроса
        titles = self.parse_page(title)

        if type(titles) is str:
            return titles
        else:
            # Проверяем правильно ли написано название
            if self.is_valid_title(title, titles):

                # Проверяем имеет ли аниме ongoing статус
                if self.is_valid_status(title):
                    # Тянем нужные нам данные
                    return self.parse_title()
                else:
                    return f"Аниме {title} не является онгоингом."
            else:
                return "Неправильное название."

