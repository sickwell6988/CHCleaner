from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.common.exceptions import *

driver = webdriver.Firefox(executable_path="c:/Users/nikita.panada/.m2/repository/webdriver/gecko/geckodriver.exe",
                           service_log_path='nul')

login_xpath = "//*[@id='loginForm']/div/div[1]/div/label/input"
pwd_xpath = "//*[@id='loginForm']/div/div[2]/div/label/input"
submit_login = "//*[@id='loginForm']/div/div[3]/button"
my_login = "nick_panada"
my_pwd = "sickwell"
search_xpath = "//*[@id='react-root']/section/div/div[1]/div/div[2]/input"
write_message_xpath = "//*[text() = 'Message']"
subscribe_xpath = "//*[text() = 'Follow']"
textarea_xpath= "//*[@id='react-root']/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea"
send_xpath = "//*[@id='react-root']/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button"

users = ['kukuha_vitebsk', 'asd', 'deborah_reed_']

message_patterns = ['Хэй! Могу безопасно и быстро накрутить подписчиков в Clubhouse. Профили реальных людей, первые 50 бесплатно (в кач-ве теста и демо). Скорость подписок = 50 чел в час. Заинтересовало?', 'Привет! Могу безопасно и быстро накрутить подписчиков в Clubhouse. Профили реальных людей, первые 50 бесплатно (в кач-ве теста). Скорость = 50чел/час. Заинтересовало?', 'Привет! Могу безопасно и быстро (50 чел в час) накрутить подписчиков в Clubhouse. Профили реальных людей + первые 50 бесплатно (в кач-ве теста/ демо). Заинтересовало?']


def open_direct():
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(5)


def close_popup():
    if driver.find_element_by_xpath("//*[text() = 'Not Now']").is_displayed():
        driver.find_element_by_xpath("//*[text() = 'Not Now']").click()


def back_to_init_page():
    open_direct()
    close_popup()


def login():
    driver.get("http://www.instagram.com")
    # assert "Python" in driver.title
    time.sleep(5)
    login = driver.find_element_by_xpath(login_xpath)
    login.send_keys(my_login)
    pwd = driver.find_element_by_xpath(pwd_xpath)
    pwd.send_keys(my_pwd)
    # pwd.send_keys(Keys.RETURN)
    submit = driver.find_element_by_xpath(submit_login)
    submit.click()
    time.sleep(5)
    back_to_init_page()


def send_message(message):
    textarea = driver.find_element_by_xpath(textarea_xpath)
    textarea.send_keys(message)
    send = driver.find_element_by_xpath(send_xpath)
    send.click()
    time.sleep(5)


def search_users(user_account):
    search = driver.find_element_by_xpath(search_xpath)
    search.send_keys(user_account)
    time.sleep(5)
    person = driver.find_element_by_xpath("//a[@href='/" + user_account + "/']")
    person.click()
    time.sleep(5)
    # write_message = driver.find_element_by_xpath(write_message_xpath)
    try:
        write_message = driver.find_element_by_xpath(write_message_xpath)
        write_message.click()
        time.sleep(5)
        message = random.choice(message_patterns)
        send_message(message)
    except NoSuchElementException:
        subscribe = driver.find_element_by_xpath(subscribe_xpath)
        subscribe.click()
        time.sleep(5)
        try:
            write_message = driver.find_element_by_xpath(write_message_xpath)
            write_message.click()
            time.sleep(5)
            message = random.choice(message_patterns)
            send_message(message)
        except NoSuchElementException:
            ig_file = open("ig_account_manual.txt", mode="a")
            ig_file.write(user_account + "\n")
            print("manual:" + user_account)


login()
for user in users:
    search_users(user)
    open_direct()