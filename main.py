from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import json
import os.path
import time


# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
#                           desired_capabilities=DesiredCapabilities.FIREFOX)

configPath = './config.json'


def read_config():
    global config
    if os.path.isfile(configPath):
        with open(configPath) as data_file:
            config = json.load(data_file)
    else:
        print('config.json file not exist')
        exit(1)


def login():
    driver.get(config['profileAddress'])
    form = driver.find_element_by_name('LoginForm')
    form.find_element_by_name("StID").send_keys(config['userName'])
    form.find_element_by_name("DummyVar").send_keys(config['password'])
    form.find_element_by_name("captchaCode").send_keys(
        input('enter captcha: '))

    form.submit()
    print(config['userName'])
    # return True

    if 'رمز ورود کاربر اشتباه است' in driver.page_source:
        print('Invalid Username')
        return False
    else:
        return True


def select_unit():
    driver.get(config['unitSelectAddress'])

    # if driver.title != "انتخاب واحد":
    #     print("ERROR - cant open unit select page")
    #     return

    # if "عدم قبول درخواست" in driver.page_source:
    #print("Select unit not started")
    # print("انتخاب واحد شروع نشده است")
    # return

    lessons = config['lessons']

    # for _ in range(3):
    while True:
        try:
            form2 = driver.find_element_by_name('PreSelCoursesList')
        except NoSuchElementException:
            print("Select unit not started :(")
            driver.get(config['unitSelectAddress'])
            continue
        for lesson in lessons:
            try:
                form2.find_element_by_xpath(
                    "//*[@value='{0}']/following::td/input[@value='']".format(lesson['lessonID'])) \
                    .send_keys('{0}'.format(lesson['code']))
                print("selected: {0}".format(lesson['lessonID']))
            except NoSuchElementException:
                print('cant find lesson: {0}'.format(lesson['lessonID']))
        form2.submit()
        print('form submitted\n')
        time.sleep(3)
    print("end")
    driver.quit()


if __name__ == '__main__':
    config = None
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("network.http.pipelining", True)
    # profile.set_preference("network.http.pipelining.aggressive", True)
    # profile.set_preference("network.http.pipelining.ssl", True)
    # profile.set_preference("network.http.pipelining.maxrequests", 2)
    # profile.set_preference("permissions.default.stylesheet", 2)
    # profile.set_preference("permissions.default.image", 2)
    # profile.set_preference("javascript.enabled", False)
    # profile.set_preference('browser.cache.use_new_backend', 1)
    # driver = webdriver.Firefox(profile)

    # driver = webdriver.PhantomJS()

    driver = webdriver.Chrome('/usr/bin/chromedriver')

    driver.set_page_load_timeout(25)

    # for r in range(1):
    while True:
        try:
            read_config()
            if login():
                while True:
                    select_unit()
                    time.sleep(3)
        except TimeoutException:
            print("timeout :(")
        except NoSuchElementException:
            print('error in find element')
        except WebDriverException:
            print('error :(')
