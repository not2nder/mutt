import os
from PIL import Image

import argparse

from bs4 import BeautifulSoup

import requests
from pick import pick

from rich import print

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--title", required=False)

    args = parser.parse_args()

    os.system('cls')
    search(t=args.title)

def textBox(string):
    text  = f'╭─{''.join(['─' for i in range(len(string)+1)])}╮\n'
    text += f'│ {string} │\n'
    text += f'╰─{''.join(['─' for i in range(len(string)+1)])}╯'

    return text

def search(t):
    query = input("Buscar:") if t ==None else t

    r = f'https://lermangas.me/?s={query}&post_type=wp-manga'
    
    soup = BeautifulSoup(requests.get(r).text, 'html.parser')
    os.system('cls')

    mangas = {}
    
    for link in soup.findAll('div', class_="tab-summary"):
        mangas[link.a.getText().strip()] = link.a.get('href')

    selected = pick(list(mangas.keys()), title=textBox(f"Busca: {query} | Use J e K Para Navegar"), indicator="->")[0]
    get_chapter(mangas[selected], selected.lower().replace(' ','_'))

def get_chapter(link,title):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    ch = {}
    for c in soup.findAll('li', class_='wp-manga-chapter'):
        ch[c.a.getText().replace('\t','').replace('\n', '')] = c.a.get('href')

    selected = pick(list(reversed(ch.keys())),title=textBox("Capitulos | Use J e K Para Navegar"), indicator="->")[0]
    download(ch[selected], f'{title}_{selected.lower().replace(' ','_')}')

def download(src, name):
    soup = BeautifulSoup(requests.get(src).text, 'html.parser')

    pgs = []

    for page in soup.findAll('div',class_='page-break no-gaps'):
        pgs.append(page.img.get('src').replace('\t','').replace('\n', ''))


    for i in range(len(pgs)):
        with open(f'images/pic{i:02d}.jpg', 'wb') as handle:
            response = requests.get(pgs[i], stream=True)

            if not response.ok:
                print(response)

            print("[b][i]Fazendo Download...")

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
            os.system('cls')

    print("[b][i]Salvando Arquivo...")
    create_PDF(name)

def create_PDF(filename):
    images = [Image.open(f'./images/{i}') for i in os.listdir('./images/') if i.endswith('.jpg')]
    images[0].save(f"./output/{filename}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
    for file in os.listdir('./images/'):
        if file.endswith('.jpg'):
            os.remove(f'./images/{file}')

if __name__ == '__main__':
    main()
