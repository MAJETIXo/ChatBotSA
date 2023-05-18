from datetime import date
import datetime
import selenium.common
from parser.init_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Класс для парсинга метаданных определенного сериала
class Serials(Parser):

    # Парсим результаты поиска
    def parse_page(self, title: str) -> selenium.webdriver:

        self.driver.get(self.url)

        input = self.driver.find_element(By.CLASS_NAME, "SearchField-input")
        input.send_keys(title)
        input.send_keys(Keys.ENTER)

        time.sleep(1) #Это нужно поправить!!!

        element = self.is_valid_title(title)

        return element

    # Проверяем существует ли такой сериал в принципе
    def is_valid_title(self, title: str) -> selenium.webdriver:
        check_title = self.driver.find_elements(By.CLASS_NAME, "ShowCol-title")
        for element in check_title:
            if title.lower() == element.text.lower():
                return element

    # Проверяем выпускается ли сериал, зачем следить за сериалом, который итак закрыт?
    @staticmethod
    def is_valid_status(element: selenium.webdriver) -> str or selenium.webdriver:
        try:
            status = element.find_element(By.CLASS_NAME, "_dead")
        except selenium.common.exceptions.NoSuchElementException:
            status = "Fine"

        return status

    # Собираем данные о сериале
    def parse_title(self) -> list or str:
        name = self.driver.find_element(By.CLASS_NAME, "title__main").text
        attrs = self.driver.find_elements(By.CLASS_NAME, "info-row")

        genres = None
        rating = None

        for attr in attrs:
            if "Жанры" in attr.text:
                genres = attr.text[7:]

            if "Рейтинг IMDB" in attr.text:
                rating = attr.text[14:attr.text.find("из") - 1]

        release = self.get_release()

        if release == "Wrong":
            return "Что-то пошло не так с поиском даты для сериала :("

        if release:
            data = [name, rating, genres, release]
            return data
        else:
            return f"Сериал {name} будет продолжен, но неизвестны даты выхода новых серий, поэтому я пока не могу добавить его"\
                    " в список отслеживаемого :("

    # Отдельный метод для получения списка дат выхода следующих серий
    def get_release(self) -> str:
        try:
            self.driver.find_element(By.CLASS_NAME, "episodes-by-season__season-row_toggle-icon").click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "episode-col__date"))
            )
        except selenium.common.TimeoutException:
            return "Wrong"

        release = self.driver.find_elements(By.CLASS_NAME, "episode-col__date")

        release_dates = []

        for element in release:
            try:
                if datetime.datetime.strptime(element.text, '%d.%m.%Y').date() > date.today():
                    release_dates.append(element.text)
                else:
                    break
            except ValueError:
                break

        if release_dates:
            return str(datetime.datetime.strptime(release_dates[len(release_dates) - 1], '%d.%m.%Y').date())

    # Складываем все воедино
    def run(self, title: str) -> list or str:
        # Получаем результат поиска
        element = self.parse_page(title)

        # Проверяем нашли ли мы тот сериал, что нам нужен
        if element:

            # Проверяем статус сериала
            if self.is_valid_status(element) == "Fine":
                element.find_element(By.TAG_NAME, "a").click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ShowDetails-poster"))
                )

                # Тянем из него нужные данные
                data = self.parse_title()

                return data

            else:
                return f"Сериал {title} уже закрыли."
        else:
            return "Не знаю такого сериала."