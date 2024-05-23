from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
import time


class NewsFetcher():
    def __init__(self, user_name, project_name, firefox_path):
        self.__user_name = user_name
        self.__firefox_path = firefox_path
        self.__project_name = project_name
        self.__title = ""
        self.__description = ""
        self.__text = ""
        self.__images_list = []

    def run(self):
        self.scrape_news_data()
        self.find_relevant_google_images()
        return self.__title, self.__description, self.__text, self.__images_list


    def scrape_news_data(self):
        profile = webdriver.FirefoxProfile(
            'C://Users/' + self.__user_name + '/AppData/Roaming/Mozilla/Firefox/Profiles/' + self.__firefox_path)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired, executable_path="C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\utils\\geckodriver.exe")

        driver.get("https://people.com/celebrity/")
        time.sleep(3)
        href_list = []
        for num in range(1, 4):
            href = driver.find_element("xpath", "/html/body/main/section/div[3]/section/div[1]/a[" + str(
                num) + "]").get_attribute("href")
            href_list.append(href)
        for num1 in range(1, 6):
            for num2 in range(1, 13):
                href = driver.find_element("xpath", "/html/body/main/section/div[3]/div/div[" + str(num1) + "]/div[1]/a[" + str(num2) + "]").get_attribute("href")
                href_list.append(href)

        z = 0
        f = open("utils/used_links.txt", 'r')
        used_links = f.readlines()
        f.close()

        for href in href_list:
            ok = 0
            for link in used_links:
                if href +"\n"== link:
                    ok = 1
            if ok == 0:
                break
            else:
                z += 1
        if len(href_list) <= z:
            print('NO NEWS AVAILABLE')
            driver.close()
            return 0
        f = open("utils/used_links.txt", 'a')
        f.write(href_list[z])
        f.write("\n")
        f.close()
        driver.get(href_list[z])
        time.sleep(4)
        try:
            link = driver.find_element("xpath", '//*[@id="figure-article_1-0"]/div/div/img').get_attribute("src")
            self.__images_list.append(link)
        except:
            pass

        try:
            self.__description = driver.find_element("id", "article-subheading_1-0").text + "\n"
        except:
            self.__description = "\n"
        paragraphs = 0

        for x in range(1, 100):
            try:
                self.__text += driver.find_element("xpath", "/html/body/main/article/div[2]/div/div[1]/p[" + str(x) + "]").text
                self.__text += "\n"
                paragraphs += 1
                if paragraphs <= 2:
                    self.__description += driver.find_element("xpath", "/html/body/main/article/div[2]/div/div[1]/p[" + str(x) + "]").text
                    self.__description += "\n"
            except:
                break
        try:
            self.__title = driver.find_element("id", 'article-heading_2-0').text
        except:
            try:
                self.__title = driver.find_element("id", 'article-heading_1-0').text
            except:
                self.__title = driver.find_element(By.XPATH, '//div[@id="people-article-header_1-0"]/h1').text

        driver.close()
    def replace_space_with_plus(self, text):
        replaced_text = ""
        for t in text:
            if t == ' ':
                replaced_text += '+'
            elif t == '&':
                replaced_text += "and"
            else:
                replaced_text += t
        return replaced_text

    def find_relevant_google_images(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=C:\\Users\\" + self.__user_name + "\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument(r'--profile-directory=Default')
        driver = webdriver.Chrome(executable_path="C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\utils\\chromedriver.exe", chrome_options=options)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(5)
        driver.get("https://google.com/search?q=" + self.replace_space_with_plus(self.__text) + "&tbm=isch")
        time.sleep(5)
        html = driver.page_source
        page = str(html)
        while True:
            start_index = page.find('"https://')
            if start_index == -1:
                break
            end_index = page.find('"', start_index + 1)
            if end_index == -1:
                break
            link = page[start_index + 1:end_index]
            if link.find(".jpg") != -1:
                self.__images_list.append(link)
            if len(self.__images_list) > 6:
                break
            page = page[end_index + 1:]