import logging
import os
import selenium
import datetime
import json
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from tf_workers.config import ApplicationConfig  # pylint: disable=E

config = ApplicationConfig.get_config()

BASEURL = 'https://www.exploit-db.com/google-hacking-database'
BASEDATE = datetime.datetime.strptime('2016-01-01','%Y-%m-%d')
DORK_CATEGORIES_PERMIT = ['Sensitive Directories', 
                          'Files Containing Juicy Info', 
                          'Files Containing Passwords']

log = logging.getLogger(__name__)
WORK_PTH = os.path.dirname(os.path.abspath(__file__))

class HttpRetriever():
    """Responsible for creating a webdriver object based on selenium
       package and Geckodriver headless.

    Note:
        By using it we can avoid problems on backlisting IPs

    Attributes:
        _driver (<selenium.obj>): Selenium webdriver object
    """

    def __init__(self):
        """ Load objects settings based on Geckodriver """
        self._driver = ''
        self.virtual_display = ''
        self.options = Options()
        self.options.headless = True

        self.caps = DesiredCapabilities.FIREFOX
        self.caps["firefox.page.settings.userAgent"] = '''
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'''
        self.caps['firefox.page.customHeaders.Accept-Language'] = 'en-USen;q=0.8'
        self.caps["firefox.page.settings.javascriptEnabled"] = True

    def run(self):
        """ Start a selenium webdriver thread object """
        self.virtual_display = Display(visible=0, size=(800, 600))
        self.virtual_display.start()
        self._driver = webdriver.Firefox(
            options=self.options,
            executable_path='{}/bin/headlessBrowser/geckodriver'.format(WORK_PTH),
            desired_capabilities=self.caps)
        return True

    def get_url(self, url):
        """ Retrieves page source code after sleeping 2, 3, 4 minutes
            to get the page full loaded
        """
        self._driver.get(url)
        sleep(randint(2, 4))
        return (self._driver.page_source).encode('utf-8')

    def click_next_page(self, element_str):
        element_btn = self._driver.find_element_by_id(element_str)
        element_btn.click()

    def stop(self):
        self._driver.close()
        self.virtual_display.stop()

class GHDBScrapper():
    def __init__(self):
        print('Initializing httpretriever object')
        self._driver = HttpRetriever()
        self._driver.run()
        self.file_write = 'googledorks.txt'
        self.dorkslist = []

    def _get_table_content(self, source_page):
        soup = BeautifulSoup(source_page, "html.parser")
        table = soup.find("table", {"id": "exploits-table"})
        table_body = soup.find("tbody")
        for each_dork in table_body.find_all('tr'):
            dork_content = each_dork.find_all('td')
            date = (dork_content[0].text).strip()
            dork = (dork_content[1].text).strip()
            category = (dork_content[2].text).strip()

            if category in DORK_CATEGORIES_PERMIT:
                self.dorkslist.append({'dork':dork, 'date':date, 'category':category})
            dateobj = datetime.datetime.strptime(date, '%Y-%m-%d')

        return dateobj


    def run(self):
        source = self._driver.get_url(BASEURL)
        while True:
            source = (self._driver._driver.page_source).encode('utf-8')
            dateobj = self._get_table_content(source)
            if dateobj < BASEDATE: break
            self._driver.click_next_page('exploits-table_next')

        with open(self.file_write, 'w') as _file_:
            _file_.write(json.dumps(self.dorkslist))

    def close(self):
        self._driver.stop()

if __name__ == '__main__':
    ghdb = GHDBScrapper()
    ghdb.run()
    ghdb.close()
