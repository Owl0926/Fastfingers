import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import locators


class SeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(executable_path='C:/bin/chromedriver.exe'))
        self.driver.maximize_window()
        self.driver.get(locators.main_page)

    def login(self):
        self.driver.find_element(By.CSS_SELECTOR, locators.go_to_login).click()
        self.driver.find_element(By.ID, locators.cookiebot).click()
        self.driver.find_element(By.XPATH, locators.email_field).send_keys(locators.email)
        self.driver.find_element(By.XPATH, locators.password_field).send_keys(locators.password)
        self.driver.find_element(By.XPATH, locators.confirm_login).click()

    def typing(self):
        word = self.driver.find_element(By.ID, locators.word)
        words = self.driver.find_elements(By.XPATH, locators.words)
        for i in words:
            word.send_keys(i.text + ' ')
        self.alertAccept()

    def go_to_advanced_typing_test(self):
        self.driver.get(locators.advanced_test_page)

    def alertAccept(self):
        WebDriverWait(self.driver, 100).until(EC.alert_is_present(), "Alert text : Are you afk? Your score has "
                                                                     "not been saved.")
        self.driver.switch_to.alert.accept()

    def result(self):
        accuracy = self.driver.find_element(By.XPATH, locators.accuracy).text
        correctness = self.driver.find_element(By.XPATH, locators.correct_words).text
        wrong_words = self.driver.find_element(By.XPATH, locators.wrong_words).text
        assert accuracy == "100%" and int(correctness) > 195 and wrong_words == "0"
        print("\nYou had", accuracy, "accuracy\nCorrect words:", correctness, "\nIncorrect words:", wrong_words)

    def test_typing(self):
        self.login()
        self.typing()
        self.result()

    def test_advanced_typing_test(self):
        self.login()
        self.go_to_advanced_typing_test()
        self.typing()
        self.result()
