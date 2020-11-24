#!/usr/bin/env python3

import argparse

import re
import json
from selenium import webdriver
from getpass import getpass
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-email-and-pw',action='store_true')

    email = input('Enter your email: ')
    password = getpass('Enter your password: ')

    config = parser.parse_args()


    driver = webdriver.Chrome(executable_path=binary_path)
    # driver = webdriver.Chrome('./chromedriver')
    # if config.headless: # headless does not work
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     driver = webdriver.Chrome('./chromedriver', options=chrome_options)


    driver.get("https://accounts.google.com/o/oauth2/auth/identifier?operation=login&state=google-%7Chttps%3A%2F%2Fmedium.com%2F%3Fsource%3Dlogin--------------------------lo_home_nav-----------%7Clogin&access_type=online&client_id=216296035834-k1k6qe060s2tp2a2jam4ljdcms00sttg.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fmedium.com%2Fm%2Fcallback%2Fgoogle&response_type=id_token%20token&scope=email%20openid%20profile&nonce=e3201beff5c040ce49e1db2009ebdc7db746a9b2f21b99e9f674f1a9151a328e&flowName=GeneralOAuthFlow")
    sleep(5)
    driver.find_element_by_css_selector("#identifierId").send_keys(f'{email}\n')

    driver.implicitly_wait(1)
    sleep(5)

    driver.find_element_by_css_selector("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input").send_keys(f'{password}'+'\n')
    driver.get('https://www.youtube.com/feed/channels?app=desktop')
    sleep(2)
    driver.refresh()

    for i in range(100):
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    links = [a.get('href') for a in soup.find_all('a', href=True)]

    channel_links = [link for link in links if '/channel/' in link]


    del channel_links[::2]

    # print(channel_links)

    links = soup.find_all(id='main-link', href=True)
    all_links = [ elem['href'] for elem in links ]#if '/channel/' in elem['href'] ]


    all_text = [ div.get_text() for div in soup.find_all('div', class_='style-scope ytd-channel-name')]


    all_names = [re.match('\\n\\n(.*?)\\n',text).groups()[0] for text in all_text
                if re.match('\\n\\n(.*?)\\n', text) ]
    all_names = [name for name in all_names if name]

    # print(all_names)

    print(len(all_links))

    print(len(all_names))
    print(len(all_names) == len(all_links))

    if len(all_names) == 0 or len(all_links) == 0:
        print('Please try again. Sometimes there are issue with the youtube page.')
    subscriptions= [{"service_id":0, "url":f'https://www.youtube.com{link}', "name":name} for name, link in list(zip(all_names, all_links))]

    new_pipe_text = { "app_version":"0.20.3","app_version_int":957, "subscriptions" : subscriptions}


    out_file = open("subscriptions.json", "w", encoding ='utf8')

    json.dump(new_pipe_text, out_file, indent = 4, ensure_ascii = True)

    out_file.close()
    print('subscriptions.json was created.')

if __name__ == "__main__":
    main()
# print(json.dumps(new_pipe_text))
