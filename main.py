# python script to take movie names from an imdb link, and then download it.
# for educational purposes only.
# qbittorrent needs to be downloaded and configured. https://www.qbittorrent.org/   https://www.thepythoncode.com/article/download-torrent-files-in-python
# default login credentials to be used.

from telnetlib import EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import urllib.request
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC


list_name = []
list_year = []
list_torrent = []
count = 0

print("Enter IMBD movies list or chart link: ")
movielist_url = input()
#movielist_url = "https://www.imdb.com/chart/top/"
print("Enter no of movies in that list or to be downloaded: ")
n = int(input())
#n = 5
print("Enter destination of movies: ")
path = input()
#path = "C:\MovieTorrents"


# download preferences
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": path}  # downloaded file location
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.headless = True           #comment out this line if you want the chrome pop up

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=chromeOptions)
chromeOptions = webdriver.ChromeOptions()
driver.set_window_size(1024, 600)
driver.maximize_window()




def movielist():
    driver.get(movielist_url)
    print(f"Link given is: {movielist_url}")
    print(f"Number of movies: {n}")
    i = 1
    time.sleep(5)
    while i <= n:
        #getting movie name
        name = driver.find_element_by_xpath(f"/html/body/div[4]/div/div[2]/div[3]/div/div[1]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/a").get_attribute("innerHTML")
        year = driver.find_element_by_xpath(f"/html/body/div[4]/div/div[2]/div[3]/div/div[1]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/span").get_attribute("innerHTML")
        year = year.replace("(", "").replace(")", "")
        name = name.replace(" ", "-").replace("'", "").replace(":", "")
        name = name.replace("--", "-")
        name = name.lower()
        list_name.append(name)
        list_year.append(year)
        print(name + " " + year)
        i = i + 1
        # time.sleep(1)
    print("Got the movies moving on to the torrenting site. ")



def downloader(downloader_url):
    # driver.get(downloader_url)
    global count
    i = 0
    while i <= n - 1:
        driver.get(f"{downloader_url}{list_name[i]}-{list_year[i]}")
        try:
            #getting torrent link
            driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div[2]/button").click()
            driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/div[1]/a[1]").click()
            #torrent = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div[3]/div[2]/div/div[1]/a[1]").get_attribute("href")
            print(f"{downloader_url}{list_name[i]}-{list_year[i]} has been found.")
        except NoSuchElementException:
            print(f"{downloader_url}{list_name[i]}-{list_year[i]} has not been found.")
            count = count + 1
        list_torrent.append(torrent)
        i = i + 1
        time.sleep(3)



def torrent():
    mis = 0
    arr = os.listdir(path)
    driver.get("http://127.0.0.1:8080/")
    print("Reached torrent client site. ")
    #default login credentials
    username = driver.find_element_by_xpath("//*[@id='username']")
    username.send_keys("admin")
    password = driver.find_element_by_xpath("//*[@id='password']")
    password.send_keys("adminadmin")
    driver.find_element_by_xpath("//*[@id='login']").click()
    print("Default login details entered and logged in. ")
    time.sleep(2)
    i = 0
    while i <= n - 1:
        driver.find_element_by_xpath("//*[@id='uploadButton']").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]/div/div/iframe")))
        location = driver.find_element_by_xpath("/html/body/form/fieldset/table/tbody/tr[2]/td[2]/input")
        location.clear()
        location.send_keys(path)
        try:
            #downloading torrents
            input = driver.find_element_by_xpath("/html/body/form/div/input")
            input.send_keys(f"{path}\{arr[i]}")
        except IndexError:
            print(f"Missing File number {i}")
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/form/fieldset/div/button").click()
        time.sleep(2)
        try:
            print(f"{arr[i]} has started downloading. ")
        except IndexError:
            mis = mis + 1
        print(f"{mis} Missing Files.")
        i = i + 1



movielist()
downloader("https://yts.rs/movie/")                                             #site for getting torrents
torrent()
#list()