import os
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import tomd
import re


def get_image(title, html):
    images = html.find('div', {'id': 'content_views'}).findAll("img")
    for img in images:
        img_url = img.get('src')
        if img_url is not None:
            file_name = img_url.split('?')[0]
            file_name = file_name.split('/')[-1]
            path = './content/' + title

            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, file_name)
            urlretrieve(img_url, file_path)
            print(file_name, ' 已下载')


def replace_h_tags(html):
    h_tags = html.findAll(re.compile(r'h\d+'))
    for h in h_tags:
        if h.find('a'):
            h.a.extract()


def clean_tags(html):
    invalid_tags = ['b', 'i', 'u', 'em', 'br', 'p']
    for tag in invalid_tags:
        for match in html.find('div', {'id': 'content_views'}).findAll(tag):
            match.replaceWithChildren()


def get_url_content(url):
    str_html = requests.get(url)
    html = BeautifulSoup(str_html.text, 'html.parser')
    title = html.find('h1').text
    date = html.find('span', {'class': 'time'}).text

    html.find('div', {'class': 'toc'}).decompose()
    html.find('svg').decompose()
    html.find('br').decompose()

    clean_tags(html)
    replace_h_tags(html)
    get_image(title, html)

    content = ''.join(map(str, html.find('div', {'id': 'content_views'}).contents))
    print(content)
    exit()
    md_content = tomd.convert(content)

    path = './content'
    file = title + '.md'
    file_path = path + '/' + file
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(file_path, 'w', encoding="utf-8")
    f.write(str(md_content))
    f.close()


def main():
    get_url_content('https://blog.csdn.net/weixin_44518486/article/details/101194267')


if __name__ == '__main__':
    main()
