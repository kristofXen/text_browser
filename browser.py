
import sys
import os
from collections import deque
# import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here


def create_dir(url):
    if os.access(url, mode=os.F_OK):
        pass
    else:
        os.mkdir(url)


def save_page(dir_url, page, page_content):
    if dir_url.endswith('/'):
        pass
    else:
        dir_url = dir_url + '/'
    page_name = page.split('.')
    if len(page_name) == 2:
        page_name = page.split('.')[0]
    else:
        # page_name = ''.join(page_name[:-1])
        page_name = page.split('.')[0]
    # print(page_name)
    with open(dir_url+page_name, 'w', encoding='utf-8') as page_file:
        page_file.write(page_content)


def open_saved_page(dir_url, ui):
    if dir_url.endswith('/'):
        pass
    else:
        dir_url = dir_url + '/'

    with open(dir_url + ui, 'r') as page_file:
        return page_file.read()

# The web
# the_web = dict()
# the_web['nytimes.com'] = nytimes_com
# the_web['bloomberg.com'] = bloomberg_com


def _print(htlm):
    soup = BeautifulSoup(htlm, 'html.parser')
    # sc = soup.contents
    # for e in sc:
    #     print(e)
    #     print('__')
    hr_txt = soup.get_text()
    print(hr_txt)
    return hr_txt


def __print(html):
    soup = BeautifulSoup(html, 'html.parser')
    rec_print(soup)


def rec_print(tag, is_in_link=False):
    if tag.name == 'a':
        is_in_link = True
    try:
        children = tag.contents
    except AttributeError:
        if is_in_link:
            print(Fore.BLUE + str(tag))
        else:
            print(tag)
    else:
        for child in children:
            rec_print(child, is_in_link)

def request_page(url):
    # check url
    if url.startswith('https://'):
        pass
    else:
        url = 'https://' + url

    # make request
    r = requests.get(url)
    # r.encoding = 'utf-8'
    content = r.content

    return content


def show_previous_page():
    global session_stack
    try:
        print(session_stack.pop())
    except IndexError:
        pass


# the browser
def quit_browser():
    sys.exit(0)


browser_instr = dict()
browser_instr['exit'] = quit_browser
browser_instr['back'] = show_previous_page

session_stack = deque()


def browser_loop(dir_url):
    global session_stack

    previous_page = ''

    while True:
        # print(session_stack)
        user_inp = input()
        # print('user ip', user_inp)
        try:
            browser_instr[user_inp]()
        except KeyError:
            try:
                # page = the_web[user_inp]
                page_content = request_page(user_inp)
                hr_txt = _print(page_content)
                __print(page_content)
                save_page(dir_url, user_inp, hr_txt)
                if previous_page == '':
                    previous_page = hr_txt
                else:
                    session_stack.append(previous_page)
                    previous_page = hr_txt
            except (KeyError, requests.exceptions.RequestException,
                    requests.exceptions.ConnectionError):
                try:
                    page_hr_txt = open_saved_page(dir_url, user_inp)
                    # print('FROM FILE')
                    print(page_hr_txt)
                except FileNotFoundError:
                    print('Invalid URL')


if __name__ == '__main__':
    # cmd args
    url_arg = sys.argv[1]
    # print(url_arg)
    create_dir(url_arg)

    # browser loop
    browser_loop(url_arg)
