#!/usr/bin/env python3
# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service

import time
import os
import sys

import requests
import pickle

COOKIE_FILE = "cookie.dump"
HOME_URL = "https://eref.thieme.de/"
AUTH_COOKIE_NAME = "THIEME_SSO"
SAVE_PATH = os.path.join(os.getcwd(), "pdf")


def load_site(url, browser, cookie=None, delete_all_cookies=False):
    browser.execute_script("window.open('');")
    time.sleep(.8)
    browser.close()
    time.sleep(.8)
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(.8)
    try:
        browser.get(url)
        time.sleep(.8)
        if delete_all_cookies:
            browser.delete_all_cookies()
        if cookie:
            browser.add_cookie(cookie)
        if "Fehler" in browser.title:
            return False
        return True
    except TimeoutException:
        # should be downloaded so it is ok
        return True


def check_url(part, cookie, try_num=0):
    url = URL % part
    if try_num == 0:
        print("Check: " + url, end="")

    try:
        response = requests.get(url, cookies={cookie["name"]: cookie["value"]})
    except requests.exceptions.TooManyRedirects:
        print(" -> Authentication failed")
        print("Invalid auth data, reauth...")
        raise NeedReAuth

    result = response.status_code != 404

    if not result and try_num < 1:
        return check_url(part, cookie, try_num + 1)
    elif not result:
        print(" -> skip (404)")
        return False
    else:
        result = download(url)
        if not result:
            print(" -> Error")
            raise ValueError
        else:
            print(" -> Success")
        return result


def download(url, try_num=0):
    result = load_site(url, web)
    if not result and try_num < 2:
        time.sleep(.8)
        return download(url, try_num + 1)
    return result


def do_auth():
    load_site(HOME_URL, web, delete_all_cookies=True)
    print("Please log in")
    input("Logged in? : Press a key")
    cookies = web.get_cookies()

    for cookie in cookies:
        if cookie["name"] == AUTH_COOKIE_NAME:
            with open(COOKIE_FILE, 'wb') as file:
                pickle.dump(cookie, file)
            print("Cookie: " + str(cookie))
            return cookie
    for cookie in cookies:
        if cookie["name"] == "JSESSIONID":
            with open(COOKIE_FILE, 'wb') as file:
                pickle.dump(cookie, file)
            print("Cookie: " + str(cookie))
            return cookie
    raise Exception


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_ebook_suffix():
    value = input("ebook suffix with format like 'ebooks/pdf/1120492/240460103%s.pdf': ")
    if not value.endswith(".pdf"):
        print("Invalid! Must end with .pdf")
        return get_ebook_suffix()
    return value


class NeedReAuth(Exception):
    pass


ebook_suffix = get_ebook_suffix()
URL = HOME_URL + ebook_suffix

try:
    os.mkdir(SAVE_PATH)
    print("Directory '% s' created" % SAVE_PATH)
except FileExistsError:
    pass

options = webdriver.FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference('browser.download.dir', SAVE_PATH)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
options.set_preference("browser.helperApps.alwaysAsk.force", False)
options.set_preference("browser.download.manager.showAlertOnComplete", False)
options.set_preference("pdfjs.disabled", True)
options.set_preference("plugin.disable_full_page_plugin_for_types",
                       "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
service = Service(resource_path('./driver/geckodriver.exe'))
web = webdriver.Firefox(service=service, options=options)
web.set_page_load_timeout(4)

try:
    with open(COOKIE_FILE, 'rb') as f:
        auth = pickle.load(f)
    load_site(HOME_URL, web, cookie={'name': auth["name"], 'value': auth["value"]})
    print("Cookie: " + str(auth))
except FileNotFoundError:
    auth = do_auth()

item = list()
for x in range(1, 1000):  # all possibilities ( 001 - 999 )
    item.append(str(x).zfill(3))

download_count = 0
error_count = 0
no_success_counter = 0
BREAK = False

for x1 in item:
    if BREAK and no_success_counter > 0:
        no_success_counter -= 1
        break
    elif BREAK:
        BREAK = False
    try:
        success = check_url("_" + x1, auth)
    except NeedReAuth:
        auth = do_auth()
        success = check_url("_" + x1, auth)
    except ValueError:
        error_count += 1
        success = False
    if not success:
        no_success_counter += 1
    else:
        no_success_counter = 0
        download_count += 1
    for x2 in item:
        if BREAK and no_success_counter > 0:
            no_success_counter -= 1
            break
        elif BREAK:
            BREAK = False
        try:
            success = check_url("_" + x1 + "_" + x2, auth)
        except NeedReAuth:
            auth = do_auth()
            success = check_url("_" + x1 + "_" + x2, auth)
        except ValueError:
            error_count += 1
            success = False
        if not success:
            no_success_counter += 1
        else:
            no_success_counter = 0
            download_count += 1
        for x3 in item:
            if BREAK and no_success_counter > 0:
                no_success_counter -= 1
                break
            elif BREAK:
                BREAK = False
            try:
                success = check_url("_" + x1 + "_" + x2 + "_" + x3, auth)
            except NeedReAuth:
                auth = do_auth()
                success = check_url("_" + x1 + "_" + x2 + "_" + x3, auth)
            except ValueError:
                error_count += 1
                success = False
            if not success:
                no_success_counter += 1
            else:
                no_success_counter = 0
                download_count += 1
            for x4 in item:
                try:
                    success = check_url("_" + x1 + "_" + x2 + "_" + x3 + "_" + x4, auth)
                except NeedReAuth:
                    auth = do_auth()
                    success = check_url("_" + x1 + "_" + x2 + "_" + x3 + "_" + x4, auth)
                except ValueError:
                    error_count += 1
                    success = False
                if not success:
                    BREAK = True
                    break
                else:
                    no_success_counter = 0
                    download_count += 1

print("DONE!")
print(str(download_count) + " files downloaded")
print("with " + str(error_count) + " errors")
web.quit()
