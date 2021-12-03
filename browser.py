import sys
import os
from collections import deque
import requests

from bs4 import BeautifulSoup


def make_readable(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()


def file_save(name, content):
    content = make_readable(content)
    #soup = BeautifulSoup(content, 'html.parser')
    #tags = soup.find_all()
    with open(name, 'w', encoding='utf-8') as file:
        #for tag in tags:
            #if tag.name == 'a':
            #    file.write(Fore.BLUE + tag.text)
            #else:
                #file.write(tag.text)
        file.write(content)


def file_read(name):
    with open(name, 'r', encoding='utf-8') as file:
        print(file.read())


def add_https(name):
    if not name.startswith('https'):
        name = 'https://' + name
    return name


def get_resp_content(url):
    response = requests.get(url)
    return response.content


def check_resp(url):
    if requests.get(url):
        return True
    else:
        return False


def url_strip(url):
    return url.lstrip('https://www.').replace('.', '_')


def main():
    dir_name = "tabs"

    if not os.access(dir_name, os.F_OK):
        os.mkdir(dir_name)
    os.chdir(dir_name)

    page_stack = deque()
    prev = 0

    while True:
        _url = input("URL or tab name (or exit/back): ")
        if _url == "exit":
            break
        elif _url == "back":
            try:
                file_name = page_stack.pop()
                file_read(file_name)
            except IndexError:
                print("Error: Nothing to go back to.")
                pass
        elif '.' in _url:
            _url = add_https(_url)
            if check_resp(_url):
                if prev != 0:
                    page_stack.append(prev)
                prev = url_strip(_url)

                file_save(prev, get_resp_content(_url))
                file_read(prev)
            else:
                print(f"Error: {requests.get(_url).status_code}")

        else:
            if os.access(_url, os.F_OK):
                file_read(_url)
            else:
                print("Error: Incorrect URL")


if __name__ == "__main__":
    main()
