
from selenium import webdriver
import time
import os
import selenium.common.exceptions

class Whatsapp():
    """
    This is Whatsapp automation using selenium in web.whatsapp.com
    How does it work?

        1. Find the directory to store all data history
        2. Connect to selenium web browser using chromedriver.exe
        3. Direct to the web.whatsapp.com
        4. Finding the target message
        5. Sending the message
        6. Close the web browser


    """
    def send_message(self, message, contact):
        """

        :param message: message that wants to be sent which is the lists of anime title
        :param contact: person that will be sent information about the anime is released which is the name of the contact
        :return: nothing
        """

        ###########################################################################################################
        # 1. Configure the web browser's option and directory to store all data history
        url = "https://web.whatsapp.com/"
        dir_path = os.getcwd()
        profile = os.path.join(dir_path, "profile", "wpp")
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir={}".format(profile))
        ###########################################################################################################


        ###########################################################################################################
        # 2. Connect to selenium web browser using chromedriver.exe
        self.driver = webdriver.Chrome(chrome_options=options)
        ###########################################################################################################


        ###########################################################################################################
        # 3. Direct to web.whatsapp.com
        self.driver.get(url)
        time.sleep(5)
        ###########################################################################################################


        ###########################################################################################################
        # 4. Finding the target message
        try:
            target = self.driver.find_element_by_xpath(f"//*[@title='{contact}']")
            target.click()
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(10)
            target = self.driver.find_element_by_xpath(f"//*[@title='{contact}']")
            target.click()
        ###########################################################################################################


        ###########################################################################################################
        # 5. Sending the message
        self.driver.find_element_by_xpath('//*[@id = "main"]/footer/div[1]/div[2]/div/div[2]').send_keys(message)
        self.driver.find_element_by_xpath('//*[@id = "main"]/footer/div[1]/div[3]/button/span').click()
        print("send succesfully")
        ###########################################################################################################


        ###########################################################################################################
        # 6. Close the web browser
        self.driver.quit()
        ###########################################################################################################











