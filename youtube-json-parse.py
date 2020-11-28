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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scroll', default='100', type=int)

    config = parser.parse_args()


    driver = webdriver.Chrome(executable_path=binary_path)
    # driver = webdriver.Chrome('./chromedriver') # local driver


    print('1. Go to https://medium.com/')
    print('2. Click on Sign In')
    print('3. Sign In with Google')
    print('Even if the message "Sorry, we didn’t recognize that account." comes,\n you are logged in.')
    print('Quick Check: If you can see your icon next to the url bar, then you are logged in\n')
    print('----------')
    input('Press enter if you are logged into google')
    driver.get('https://www.youtube.com/feed/channels?app=desktop')
    sleep(2)
    driver.refresh()

    for i in range(config.scroll):
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

    print('Number of channel links: ', len(all_links))

    print('Number of channel names: ', len(all_names))
    print('Are the number of links and names equal?: ', len(all_names) == len(all_links))

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
