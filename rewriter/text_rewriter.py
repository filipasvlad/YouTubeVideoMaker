import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import emoji
import time


class TextRewriter():
    def __init__(self, user_name, project_name, firefox_path):
        self.__user_name = user_name
        self.__project_name = project_name
        self.__firefox_path = firefox_path

    def run(self, title, description, text):
        title = self.text_without_emoji(title)
        description = self.text_without_emoji(description)
        text = self.text_without_emoji(text)
        self.rewrite_text(title, description, text)
        title = self.shorten_title(title)
        return title, description, text

    def rewrite_text(self, title, description, text):
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=C:\\Users\\" + self.__user_name + "\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument(r'--profile-directory=Default')
        driver = webdriver.Chrome(executable_path="C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\utils\\chromedriver.exe", chrome_options=options)
        driver.get("https://quillbot.com/paraphrasing-tool")
        driver.maximize_window()
        time.sleep(5)
        # CLOSE RECLAME
        try:
            driver.find_element("xpath", "/html/body/div[6]/div[3]/div/div[1]/button").click()
        except:
            pass
        time.sleep(3)
        for y in range(4, 10):
            for z in range(4, 10):
                try:
                    driver.find_element("xpath",
                                        "/html/body/div[" + str(z) + "]/div[3]/div/div[1]/button").click()
                    time.sleep(5)
                except:
                    pass
                try:
                    driver.find_element("xpath",
                                        "/html/body/div[" + str(z) + "]/div[3]/div/div/div[1]/button").click()
                    time.sleep(5)
                except:
                    pass
        time.sleep(5)

        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).clear()
        time.sleep(5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).send_keys(title)
        time.sleep(3)

        driver.find_element("xpath", '//*[@id="pphr-view-input-panel-footer-box"]/div[2]/div/button').click()

        time.sleep(20)
        try:
            driver.find_element("xpath", "/html/body/div[1]/div[2]/div[3]/section[1]/div/div/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div/button").click()
        except:
            pass
        try:
            driver.find_element("xpath", "//*[@aria-label='Copy Full Text']").click()
        except:

            driver.close()
            return self.rewrite_text(title, description, text)

        time.sleep(2)
        title = pyperclip.paste()

        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).clear()
        time.sleep(5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).send_keys(description)
        time.sleep(3)

        driver.find_element("xpath", '//*[@id="pphr-view-input-panel-footer-box"]/div[2]/div/button').click()

        time.sleep(20)
        try:
            driver.find_element("xpath",
                                "/html/body/div[1]/div[2]/div[3]/section[1]/div/div/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div/button").click()
        except:
            pass
        try:
            driver.find_element("xpath", "//*[@aria-label='Copy Full Text']").click()
        except:
            driver.close()
            return self.rewrite_text(title, description, text)

        time.sleep(2)
        description = pyperclip.paste()

        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).clear()
        time.sleep(5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).send_keys(text)
        time.sleep(3)

        driver.find_element("xpath", '//*[@id="pphr-view-input-panel-footer-box"]/div[2]/div/button').click()

        time.sleep(20)
        try:
            driver.find_element("xpath",
                                "/html/body/div[1]/div[2]/div[3]/section[1]/div/div/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div/button").click()
        except:
            pass
        try:
            driver.find_element("xpath", "//*[@aria-label='Copy Full Text']").click()
        except:
            driver.close()
            return self.rewrite_text(title, description, text)

        time.sleep(2)
        text = pyperclip.paste()
        return title, description, text

    def shorten_title(self, title):
        if len(title) < 100:
            return title
        else:
            number = 97
            while title[number] != ' ':
                number -= 1
            number -= 1
            title = title[:number + 1]
            title += '...'
            return title

    def text_without_emoji(self, text):
        return emoji.replace_emoji(text, replace='')