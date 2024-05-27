import os
import sys

from bs4 import BeautifulSoup

import requests
from pick import pick

from rich import print
from rich.console import Console

console = Console()

def main():
    os.system('cls')
    search()

def search():
    print('[r][b]Pesquisar:')
    query = input(":")
    r = f'https://mangapill.com/search?q={query}'
    
    soup = BeautifulSoup(requests.get(r).text, 'html.parser')
    os.system('cls')

    mangas = {}
    
    for link in soup.findAll('div', class_="flex flex-col justify-end"):
        mangas[link.a.getText().strip()] = link.a.get('href')
    selected = pick(list(mangas.keys()),"Escolhe ai", indicator="->")[0]
    get_chapter(mangas[selected])


def get_chapter(link):
    r = f'https://mangapill.com/{link}'
    soup = BeautifulSoup(requests.get(r).text, 'html.parser')
    ch = {}

    for c in soup.findAll('a', class_='border border-border p-1 hover:bg-brand hover:text-white'):
        ch[c.getText()] = c.get('href')
    
    selected = pick(list(reversed(ch.keys())),"Escolhe ai", indicator="->")[0]
    print(selected)

if __name__ == '__main__':
    main()