from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import json
import os.path


# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
#                           desired_capabilities=DesiredCapabilities.FIREFOX)


def login():
    driver.get(config['profileAddress'])
    form = driver.find_element_by_name('LoginForm')
    form.find_element_by_name("StID").send_keys(config['userName'])
    form.find_element_by_name("DummyVar").send_keys(config['password'])
    form.submit()
    # return True

    if 'رمز ورود کاربر اشتباه است' in driver.page_source:
        print('Invalid Username')
        return False
    else:
        return True


def fill_form():
    driver.get(config['shahrieAddress'])
    lessons = config['lessons']
    form = driver.find_element_by_name('PreCalcTuition')

    for lesson in lessons:
        try:
            xpath = "//input[@value='{0}']/parent::tr/td[1]/input".format(
                lesson['lessonID'])
            form.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            print('cant find lesson: {0}'.format(lesson['lessonID']))
    form.submit()
    print('form submitted')
    print("end")
    # driver.quit()


def foo():
    print('\nstart')
    lessons = config['lessons']
    for i in range(len(lessons)):
        lesson = lessons[i]
        print('i:{0} id:{1} code:{2}'.format(
            i, lesson['lessonID'], lesson['code']))
    print('finish')


def read_config():
    global config
    if os.path.isfile('./shahrie.json'):
        with open('shahrie.json') as data_file:
            config = json.load(data_file)
    else:
        print('shahrie.json file not exist')
        exit(1)


if __name__ == '__main__':
    config = None
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.http.pipelining", True)
    profile.set_preference("network.http.pipelining.aggressive", True)
    profile.set_preference("network.http.pipelining.ssl", True)
    profile.set_preference("network.http.pipelining.maxrequests", 2)
    profile.set_preference("permissions.default.stylesheet", 2)
    profile.set_preference("permissions.default.image", 2)
    profile.set_preference("javascript.enabled", False)
    profile.set_preference('browser.cache.use_new_backend', 1)
    driver = webdriver.Firefox(profile)
    # driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(5)

    try:
        read_config()
        if login():
            fill_form()
    except TimeoutException:
        print("timeout :(")
    except NoSuchElementException as e:
        print('error in find element')
        print(e.msg)
        driver.quit()
    except WebDriverException:
        print('error :(')
