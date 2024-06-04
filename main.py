import os
import sys
from PIL import Image

import argparse

from time import sleep

import webbrowser

from bs4 import BeautifulSoup

import requests

from InquirerPy import inquirer
from rich import print
from rich.progress import track

path = f'{os.path.expanduser('~')}\\Documents\\mutt'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--query", required=False)

    args = parser.parse_args()

    if not(os.path.exists(path)):
        os.mkdir(path)

    os.system('cls')
    search(t=args.query)

def search(t):
    print('[bold white on #005acd] Buscar mangá [/]\n')
    query = inquirer.text(message="", qmark=">", amark=">").execute() if t == None else t

    r = f'https://lermangas.me/?s={query}&post_type=wp-manga'
    
    soup = BeautifulSoup(requests.get(r).text, 'html.parser')
    os.system('cls')

    mangas = {}
    
    for link in soup.findAll('div', class_="tab-summary"):
        mangas[link.a.getText().strip()] = link.a.get('href')
    
    if not mangas:
        print('[bold white on red] Mangá não encontrado[/]\n')
        print('Voltando para tela de busca...')
        sleep(1)
        main()

    print('[bold white on #005acd] Resultados [/]\n')

    selected = inquirer.select(
        message="Selecione o mangá: ",
        choices=list(mangas.keys()),
        multiselect=False,
        pointer="❚",
        qmark=">",
        amark=">"
    ).execute()

    get_chapter(mangas[selected], selected.lower().replace(' ','_'))

def get_chapter(link,title):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    ch = {}
    for c in soup.findAll('li', class_='wp-manga-chapter'):
        ch[c.a.getText().replace('\t','').replace('\n', '')] = c.a.get('href')
    
    selected = inquirer.select(
        message="Capítulo(s): ",
        choices=list(reversed(ch.keys())),
        multiselect=True,
        pointer="❚",
        marker=" * ",
        qmark=">",
        amark=">"
    ).execute()
    
    os.system('cls')
    print('[bold white on #005acd] Lendo [/]\n')
    for i in selected:
        print(f'[#005acd]Baixando[/] {i}')
        download(ch[i], f'{title}_{i.lower().replace(' ','_')}',title, i.lower().replace(' ','_'))
    
    sys.exit()

def download(src, title, directory, chapter):
    # src = link (https://...)
    # title = nome do pdf (Ex.: jjk_cap_1.pdf)
    # directory = pasta do manga (Ex.: jujutsu_kaisen/)
    # path pasta da aplicaçao (mutt/)
    # chapter = nome da pasta dentro de manga (Ex.: Capitulo_1/)

    if not(os.path.exists(f'{path}/{directory}')):
        os.mkdir(f'{path}/{directory}')

    soup = BeautifulSoup(requests.get(src).text, 'html.parser')

    pgs = []

    for page in soup.findAll('div',class_='page-break no-gaps'):
        pgs.append(page.img.get('src').replace('\t','').replace('\n', ''))
    
    if not(os.path.exists(f'{path}\\{directory}\\{chapter}')):
        os.mkdir(f'{path}\\{directory}\\{chapter}')

    os.mkdir(f'{path}\\{directory}\\{chapter}\\images')

    for i in track(range(len(pgs)),description=f'[#005acd]Carregando[/] {len(pgs)} páginas'):
        with open(f'{path}\\{directory}\\{chapter}\\images/pic{i:02d}.jpg', 'wb') as handle:
            response = requests.get(pgs[i], stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    print("[#005acd]Processando[/] arquivo...")
    create_PDF(title, f'{path}\\{directory}\\{chapter}')

def create_PDF(filename,directory):
    images = [Image.open(f'{directory}\\images/{i}') for i in os.listdir(f'{directory}/images/') if i.endswith('.jpg')]
    images[0].save(f"{directory}\\{filename}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
    for file in os.listdir(f'{directory}\\images'):
        if file.endswith('.jpg'):
            os.remove(f'{directory}/images/{file}')
    webbrowser.open_new(f'{directory}\\{filename}.pdf')

if __name__ == '__main__':
    main()
