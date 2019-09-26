from bs4 import BeautifulSoup

_supportTags = {
    'blockquote',
	'p',
	'a',
	'h1','h2','h3','h4','h5','h6',
	'strong','b',
	'em','i',
	'ul','ol','li',
	'br',
	'img',
	'pre','code',
	'hr',
    'kbd',
    'mark',
    's',
    'sup','sub',
    'section'
}

def _getmdchild(child,childtype=1):
    content = ''
    if _supportTags.__contains__(child.name):
        if childtype == 1:
            content += '\n\n'
        if child.name == 'h1':
            content += '# ' + child.text
        elif child.name == 'h2':
            content += '## ' + child.text
        elif child.name == 'h3':
            content += '### ' + child.text
        elif child.name == 'h4':
            content += '#### ' + child.text
        elif child.name == 'h5':
            content += '##### ' + child.text
        elif child.name == 'h6':
            content += '###### ' + child.text
        elif child.name == 'p':
            # 判断是否有子
            childs = child.children
            if childs is not None:
                for secondchild in childs:
                   content += _getmdchild(secondchild,2)
            else:
                content += child.text
        elif child.name == 'strong':
            childs = child.children
            if childs is not None:
                content += '**'
                for secondchild in childs:
                   content += _getmdchild(secondchild,2)
                content += '**'
            else:
                content += '**' + child.text + '**'
        elif child.name == 'em':
            content += '*' + child.text + '*'
        elif child.name == 'mark':
            content += '==' + child.text + '=='
        elif child.name == 's':
            content += '~~' + child.text + '~~'
        elif child.name == 'sup':
            content += '^' + child.text + '^'
        elif child.name == 'sub':
            content += '~' + child.text + '~'
        elif child.name == 'kbd':
            content += '<kbd>' + child.text + '</kbd>'
        elif child.name == 'img':
            content += '![' + child.get('alt') + '](' + child.get('src').split('?')[0] + ')' # csdn图片水印问题，截取路径?之前，?之后的为图片附加参数
        elif child.name == 'pre':
            # 判断是否有子
            childs = child.children
            if childs is not None:
                content += '\n\n'
                content += '```'
                content += '\n\n'
                for secondchild in childs:
                   content += _getmdchild(secondchild,2)
                content += '\n\n'
                content += '```'
                content += '\n\n'
        elif child.name == 'code':
            if child.parent.name == 'p':
                content += '`' + child.text + '`'
            else:
                # 判断是否有子
                childs = child.children
                if childs is not None:
                    for secondchild in childs:
                        content += _getmdchild(secondchild,2)
        elif child.name == 'ul' or child.name == 'ol':
            # 先屏蔽有些code带行号
            if child.parent.name != 'pre':
                childs = child.children
                if childs is not None:
                    if child.name == 'ol':
                        index = 1
                    for secondchild in childs:
                        if str(secondchild) == '\n':
                            continue
                        if child.name == 'ol':
                            content += '\n\n'
                            content += str(index) + '. '
                            content += _getmdchild(secondchild,2)
                            content += '\n\n'
                            index+=1
                        else:
                            content += _getmdchild(secondchild,2)
        elif child.name == 'li':
            childs = child.children
            if childs is not None:
                childtype = 1
                if child.parent.name == 'ol':
                    childtype = 2
                for secondchild in childs:
                    content += _getmdchild(secondchild,childtype)
        elif child.name == 'a':
            if child.parent.name == 'li' or child.parent.name == 'p':
                content += '[' + child.text + '](' + child.get('href') + ')'
        elif child.name == 'blockquote':
            # 判断是否有子
            childs = child.children
            if childs is not None:
                content += '> '
                for secondchild in childs:
                   content += _getmdchild(secondchild,2)
        elif child.name == 'section':
            # 判断是否有子
            childs = child.children
            if childs is not None:
                for secondchild in childs:
                   content += _getmdchild(secondchild,1)
    elif isinstance(child,str):
        if child.parent.name != 'div' and child != '\n':
            if child.parent.name == 'li' and child.parent.parent.name == 'ul':
                content += '- '
            content += child
    elif child.name == 'span':
        content += child.text
    return content

def getmdcontent(html):
        
    title = html.find('h1').text
    date = html.find('span',{'class':'time'}).text
    # print(title)
    # print(date)
    # print(len(childs))
    temphtml = html.findAll('div', {'id': 'content_views'})[0]
    # print(temphtml)
    # print(html)
    childs = temphtml.children
    mdcontent = {
        'title' : title,
        'date' : date,
        'content': ''
    }
    if childs is not None:
        content = ''
        for child in childs:
            # print(child)
            content += _getmdchild(child)
        mdcontent['content'] = content
    return mdcontent