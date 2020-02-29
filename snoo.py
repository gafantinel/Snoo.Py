#!/usr/bin/env python3
import requests
import sys
import concurrent.futures

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
    elif status ==  401 or status == 403:
        return colors.WARNING
    elif status == 404 or status == 500:
        return colors.FAIL
    else:
        return colors.ENDC

def resolver(url):
    try:
        r = requests.get(url,timeout=10)
        try:
            status = r.status_code
        except:
            status = "Unknown"
        try:
            server = r.headers['server']
        except:
            server = "Unknown"
        color = color_pick(status)

        print(f"{url}  =>  [Status: {color}{status}{colors.ENDC}, Server: {colors.BOLD}{server}{colors.ENDC}]",flush=True)
    except:
        print(f"{url}  =>  [Could not connect to the specified host]",flush=True)

def resolve_all(urls,concurrency):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        executor.map(resolver, urls)

if __name__ == "__main__":
    url_file = sys.argv[1]

    try:
        concurrency = int(sys.argv[2])
    except IndexError:
        concurrency = 5

    urls = []

    if url_file:
        try:
            with open(url_file, 'r', encoding="utf8") as file:
                for line in file:
                    urls.append(line.strip('\n'))
        except FileNotFoundError:
            print(
                """
                  \,`/ /
                 _)..  `_
                ( __  -\\
                    '`.              This file does not exist...
                   ( \>_-_,
                   _||_ ~-/
                """
            )
            exit(1)
        except KeyboardInterrupt:
            print("Exiting...")
            exit(1)
    banner()
    resolve_all(urls,concurrency)