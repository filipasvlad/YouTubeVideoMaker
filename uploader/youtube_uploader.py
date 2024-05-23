import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from textblob import TextBlob
import gspread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class YoutubeUploader():
    def __init__(self, user_name, project_name, firefox_path):
        self.__user_name = user_name
        self.__project_name = project_name
        self.__firefox_path = firefox_path

    def upload(self, title, description):
        profile = webdriver.FirefoxProfile('C://Users/' + self.__user_name + '/AppData/Roaming/Mozilla/Firefox/Profiles/' + self.__firefox_path)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired, executable_path="C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\utils\\geckodriver.exe")
        time.sleep(4)
        driver.get("https://youtube.com/upload")
        time.sleep(16)

        #Video upload
        driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input").send_keys("C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\utils\\media\\video.mp4")
        time.sleep(15)

        #Set title
        title_xpath = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
        try:
            text = driver.find_element("xpath", title_xpath).text
        except:
            title_xpath = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
            text = driver.find_element("xpath", title_xpath).text
        while text.find("finalizat") != -1:
            driver.find_element("xpath", title_xpath).clear()
            time.sleep(5)
            driver.find_element("xpath", title_xpath).send_keys(title)
            time.sleep(5)
            text = driver.find_element("xpath", title_xpath).text
        time.sleep(4)

        #Set description
        driver.find_element("xpath", '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div').send_keys(description)
        time.sleep(7)

        #Upload thumbnail
        try:
            driver.find_element("xpath", '//*[@id="file-loader"]').send_keys("C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\thumbnail.jpg")
        except:
            pass
        time.sleep(3)


        #driver.find_element("xpath", '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button/div').click()
        #time.sleep(3)
        #try:
        #    driver.find_element("xpath", '//*[@id="clear-button"]').click()
        #except:
        #    pass
        #time.sleep(3)

        #Press Next Button
        driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div").click()
        time.sleep(3)

        #Enable monetization 1
        driver.find_element("id", "child-input").click()
        time.sleep(3)
        driver.find_element("xpath",
                            "/html/body/ytcp-video-monetization-edit-dialog/tp-yt-paper-dialog/div/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]").click()
        time.sleep(3)
        driver.find_element("xpath",
                            "/html/body/ytcp-video-monetization-edit-dialog/tp-yt-paper-dialog/div/div/ytcp-button[2]/div").click()
        time.sleep(3)

        # Press Next Button
        driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div").click()
        time.sleep(5)

        # Enable monetization 2
        scrollable_element = driver.find_element("xpath", '//*[@id="scrollable-content"]')
        driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scrollable_element)
        time.sleep(5)
        driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-content-ratings/ytpp-self-certification-questionnaire/div[3]/div/ytcp-checkbox-lit/div[1]").click()
        time.sleep(5)
        driver.find_element("xpath", '//*[@id="submit-questionnaire-button"]').click()
        time.sleep(15)

        # Press Next Button
        try:
            driver.find_element("xpath", '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div').click()
        except:
            wait = WebDriverWait(driver, 100)
            element = wait.until(EC.element_to_be_clickable((By.ID, "step-badge-3")))
            element.click()
        time.sleep(8)

        #Show next video at the end of the video
        try:
            driver.find_element("id", "import-from-video-button").click()
            time.sleep(15)
            driver.find_element("xpath", "/html/body/ytve-endscreen-modal/ytve-modal-host/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/ytve-editor/div[1]/div/ytve-endscreen-editor-options-panel/div[2]/div/ytve-endscreen-template-picker/div/div/div/div[1]/div[1]").click()
            time.sleep(14)
            driver.find_element("xpath", "/html/body/ytve-endscreen-modal/ytve-modal-host/ytcp-dialog/tp-yt-paper-dialog/div[1]/div/div[2]/div[2]/ytcp-button/div").click()
            time.sleep(20)
        except:
            pass

        #Make the video public
        while True:
            try:
                driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[1]/div[1]").click()
                time.sleep(7)
                break
            except:
                # Press Next Button
                element = driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(12)

        #Press Upload
        driver.find_element("xpath", "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div").click()
        time.sleep(10)
        try:
            driver.find_element("xpath", "/html/body/ytcp-prechecks-warning-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/div/ytcp-button/div").click()
        except:
            pass
        time.sleep(18)
        driver.close()

