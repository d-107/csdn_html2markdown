import os
import re
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup, Comment

_supportTags = {
    'blockquote',
    'p',
    'a',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'b',
    'em', 'i',
    'ul', 'ol', 'li',
    'br',
    'img',
    'pre', 'code',
    'hr',
    'kbd',
    'mark',
    's',
    'sup', 'sub',
    'section'
}

ss = {
    "blockquote": ">",
    "li": "-",
    "hr": "---",
    "p": "\n"
}


def format_h_tags(html):
    markdown_h_tags = {
        'h1': "#",
        'h2': "##",
        'h3': "###",
        'h4': "####",
        'h5': "#####",
        'h6': "######",
    }

    for tag in html.findAll(re.compile(r'h\d+')):
        tag.a.extract() if tag.find('a') else ''
        tag.string = str(markdown_h_tags.get(tag.name) + ' ' + tag.text.replace("\n", ""))
        tag.replaceWithChildren()


def format_p_tags(html):
    for tag in html.findAll('p'):
        tag.replaceWithChildren()


def format_img_tags(title, html):
    for img in html.find('div', {'id': 'content_views'}).findAll("img"):
        img_url = img.get('src')
        if img_url is not None:
            file_name = img_url.split('?')[0]
            file_name = file_name.split('/')[-1]
            path = './' + title

            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, file_name)
            urlretrieve(img_url, file_path)
            img.string = '![' + img.get('alt') + '](' + file_path + ')'
            img.replaceWithChildren()


def handle(html):
    title = html.find('h1').text
    date = html.find('span', {'class': 'time'}).text
    html = BeautifulSoup(str(html.find('div', {'id': 'content_views'})), 'html.parser')

    content = """
    ---
    title: """ + title + """
    date: """ + date + """
    ---
    """

    # 去注释
    for element in html(text=lambda text: isinstance(text, Comment)):
        element.extract()

    html.find('div', {'class': 'toc'}).decompose()
    html.find('svg').decompose()
    html.find('br').decompose()

    format_h_tags(html)
    format_p_tags(html)
    format_img_tags(title, html)
    print(html)


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    url = 'https://blog.csdn.net/u012050154/article/details/77745224'
    str_html = requests.get(url, headers=headers)
    html = BeautifulSoup(str_html.text, 'html.parser')
    print(str_html.text)
    handle(html)


if __name__ == '__main__':
    main()
