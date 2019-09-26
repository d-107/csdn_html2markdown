import re

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


def clean_h_tags(html):
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


def clean_p_tags(html):
    for tag in html.findAll('p'):
        tag.replaceWithChildren()


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

    clean_h_tags(html)
    clean_p_tags(html)
    print(html)


def main():
    url = 'https://blog.csdn.net/weixin_44518486/article/details/101194267'
    str_html = requests.get(url)
    html = BeautifulSoup(str_html.text, 'html.parser')
    handle(html)


if __name__ == '__main__':
    main()
