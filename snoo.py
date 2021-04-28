#!/usr/bin/env python3
import requests
import sys
import concurrent.futures
from lxml.html import fromstring


def banner():
    print(
        f"""
            ,-.
          .:\ '`-.
          |:|  __ b
           `;-(
          ,'  |                 {colors.WARNING}{colors.BOLD}Snoo.py{colors.ENDC}
         ( \|||_
  ,-----(.-''--``-------.
 /_______`'______________\\
/                         \\
============================
        """
    )


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_pick(status):
    if status == 200:
        return colors.OKGREEN
    elif status == 301 or status == 302:
        return colors.OKBLUE
    elif status == 401 or status == 403:
        return colors.WARNING
    elif status == 404 or status == 500:
        return colors.FAIL
    else:
        return colors.ENDC


def resolver(url):
    try:

        r = requests.get(url, timeout=10, allow_redirects=redirect)
        try:
            status = r.status_code
        except:
            status = "Unknown"
        try:
            # title = r.content['title']
            content = fromstring(r.content)
            title = content.findtext('.//title').replace('\n','')
        except:
            title = "Unknown"
        try:
            server = r.headers['server']
        except:
            server = "Unknown"
        try:
            size = str(len(r.text))
        except:
            size = "Unknown"
        color = color_pick(status)
        try:
            if '301' in str(r.history[0]) or '302' in str(r.history[0]):
                print('[REDIR]',end=" ")
        except:
            a = ''
        print(
            f"{url}  {color}=>  [Status: {colors.BOLD}{status}{colors.ENDC}{color} | Title: {colors.BOLD}{title}{colors.ENDC}{color} | Server: {colors.BOLD}{server}{colors.ENDC}{color} | Size: {colors.BOLD}{size}]{colors.ENDC}", flush=True)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(1)
    except:
        print(
            f"{url}  =>  [Could not connect to the specified host]", flush=True)


def resolve_all(urls, concurrency):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        executor.map(resolver, urls)


if __name__ == "__main__":
    url_file = sys.argv[1]
    try:
        concurrency = int(sys.argv[1])
    except IndexError:
        concurrency = 5
    try:
        if (sys.argv[2] == '-r'):
            redirect = True
    except IndexError:
            redirect = False
    urls = []

    for line in sys.stdin:
        urls.append(line.strip('\n'))
    banner()
    resolve_all(urls, concurrency)
    
