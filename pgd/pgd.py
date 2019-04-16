import logging
import os
import selenium
import datetime
import json
from urllib import parse as urllib
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from tf_workers.config import ApplicationConfig  # pylint: disable=E

config = ApplicationConfig.get_config()

log = logging.getLogger(__name__)
WORK_PTH = os.path.dirname(os.path.abspath(__file__))

GOOGLEURL = 'https://www.google.com/search?q='

class PGD():
    def __init__(self, domain, google_dorks):
        self._driver = ''
        self.domain = domain
        self.dorks = google_dorks
        self.current_dork = ''
        self.virtual_display = ''
        self.options = Options()
        self.options.headless = True

        self.caps = DesiredCapabilities.FIREFOX
        self.caps["firefox.page.settings.userAgent"] = self._get_user_agent()
        self.caps['firefox.page.customHeaders.Accept-Language'] = 'en-USen;q=0.8'
        self.caps["firefox.page.settings.javascriptEnabled"] = True

        self.initialize()

    def initialize(self):
        for dork in self.dorks:
            quote_dork = urllib.quote(dork, safe='')
            self.current_dork = quote_dork

            self.run()
            self.stop()

    def _get_user_agent(self):
        with open('{}/utils/user_agents.txt'.format(WORK_PTH)) as _useragent_file_:
            content = _useragent_file_.readlines()
            return content[randint(0,len(content)-1)]

    def _get_google_next_page(self):
        try:
            element_btn = self._driver.find_element_by_id('pnnext')
            element_btn.click()
            sleep(randint(2, 4))
            return True
        except:
            return False

    def _get_dorks_from_google(self):
        next_page_exists = True
        while next_page_exists:
            source = (self._driver.page_source).encode('utf-8')
            soup = BeautifulSoup(source, "html.parser", from_encoding='utf-8')
            search_block = soup.find("div", {"id": "search"})
            try:
                if search_block.text == '':
                    print("[-] Dork {} not found!".format(urllib.unquote(self.current_dork)))
                    break
                else:
                    print("[+] Dork {} found in {}!".format(urllib.unquote(self.current_dork), self.domain))
                    for link in search_block.find_all('a'):
                        try:
                            if link.find('h3').text != '':
                                print('\t Dork found in: {}'.format(link.get('href')))
                        except:
                            pass

                        next_page_exists = self._get_google_next_page()

            except Exception as e:
                print("[-] Dork {} not found!".format(urllib.unquote(self.current_dork)))
                break

    def run(self):
        """ Start a selenium webdriver thread object """
        self.virtual_display = Display(visible=0, size=(800, 600))
        self.virtual_display.start()
        self._driver = webdriver.Firefox(
            options=self.options,
            executable_path='{}/bin/headlessBrowser/geckodriver'.format(WORK_PTH),
            desired_capabilities=self.caps)

        self._driver.get("{}{} site:{}".format(GOOGLEURL, self.current_dork, self.domain))
        sleep(randint(2, 5))
        self._get_dorks_from_google()

        return True

    def stop(self):
        self._driver.close()
        self.virtual_display.stop()

if __name__ == '__main__':
    with open('googledorks.txt','r') as _dorkfile:
        dorks = json.loads(_dorkfile.read())

    dorkslist = list(x['dork'] for x in dorks)
    ghdb = PGD('facti.com.br', dorkslist)
