#
# btbb.py
# Created by Hexapetalous on Feb 2, 2016.
#
# This is a part of P0009.
# `btbb` means 'Black Techniques of Baidu BBS.'
#
# Copyright (c) 2016 Hexapetalous. All rights reserved.
#
import requests
from bs4 import BeautifulSoup


def get_title_from_url(url):
    raw = _get_raw_text_from_url_and_page(url, 1)
    soup = BeautifulSoup(raw, 'html5lib')
    return soup.title.string


def get_url_from_tid(tid):
    if type(tid) == int and tid > 0:
        return 'http://tieba.baidu.com/p/' + str(tid)
    else:
        return ''


def get_tid_from_url(url):
    if type(url) != str or url[:25] != 'http://tieba.baidu.com/p/':
        return None
    try:
        tid = int(url[25:])
    except ValueError:
        return None
    if tid <= 0:
        return -1
    return tid


def get_total_page_count(url):
    text = get_page_raw_text(url)
    if text == '':
        return -1
    soup = BeautifulSoup(text, 'html5lib')
    # This depends on the structure of the web page.
    try:
        return int(soup('span', 'red')[1].string)
    except IndexError:
        return -1
    except ValueError:
        return -1


# Manually checking if page is out of the total before calling this function is
# necessary.
def _get_raw_text_from_url_and_page(url, page):
    p = {'pn': page}
    try:
        res = requests.get(url, params=p)
    except requests.ConnectionError:
        return ''
    return res.text


# This only get the first page.
def get_page_raw_text(url):
    try:
        res = requests.get(url)
    except requests.ConnectionError:
        return ''
    return res.text


# The return seems to be a new type, and I call it list of `Floor`.
# Set `max_*` to -1 if don't need.
def get_floors(url, max_page, max_floor):
    page_count = get_total_page_count(url)
    if page_count == -1:
        return []
    if 0 < max_page < page_count:  # What the f***...
        page_count = max_page
    result = []
    for i in range(page_count):
        text = _get_raw_text_from_url_and_page(url, i + 1)
        if text == '':
            return result
        soup = BeautifulSoup(text, 'html5lib')
        important_soup = soup('div', class_='l_post')
        for sweet_dumpling in important_soup:
            if 0 < max_floor < floor_get_floor_number(sweet_dumpling):
                return result
            result.append(sweet_dumpling)
    return result


def get_all_floors(url):
    return get_floors(url, -1, -1)


# Here are a few functions that takes a `Floor` as a argument.
def floor_get_lz(floor):  # I don't want to think of English name ANY MORE!
    return floor('a', class_='p_author_name')[0].text


def floor_get_content(floor):
    result = ''
    for c in floor('div', class_='d_post_content')[0].children:
        import bs4
        if type(c) == bs4.NavigableString:
            result += c.string.strip()
        if c.name == 'br':
            result += '\n'
        if c.name == 'a':
            result += c.string.strip()
        if c.name == 'img':
            result += '【此处应有自拍】'
    return result


def floor_get_floor_number(floor):
    return int(floor('span', class_='tail-info')[-2].text[:-1])


# Returns something like `2016-01-28 22:03`
def floor_get_time(floor):
    return floor('span', class_='tail-info')[-1].text


def floor_get_post_id(floor):
    return floor('div', class_='d_post_content')[0]['id'][13:]


# DO NOT TAKE `Floor` any more.
def get_floor_in_floor_root_url():
    return 'http://tieba.baidu.com/p/totalComment'


# This function returns a list of `Comments`.
# The comment list may be
def get_floor_in_floors(tid, max_page):
    page_count = get_total_page_count(get_url_from_tid(tid))
    if page_count == -1:
        return []
    if 0 < max_page < page_count:  # What the f***...
        page_count = max_page
    result = []
    for i in range(page_count):
        p = {'tid': tid, 'fid': 12138, 'pn': i + 1, 'see_lz': 0}
        try:
            r = requests.get(get_floor_in_floor_root_url(), params=p)
        except requests.ConnectionError:
            return []
        comment_list = r.json()['data']['comment_list']
        if type(comment_list) != dict:
            continue
        for comment in comment_list.values():
            result.append(comment)
    return result


# This function takes `Comments` as an argument.
# And return a list of `Comment`.
def comments_get_comments(cs):
    return cs['comment_info']


# These functions take `Comment` as an argument.
def comment_get_content(c):
    return c['content']


def comment_get_post_id(c):
    return c['post_id']


def d_get_rid_of_a(c):
    i = c.find('<a')
    if i == -1:
        return c
    c1 = c[:i]
    while c[i] != '>':
        i += 1
    c1 += c[i+1:]
    i = c1.find('</a>')
    c1 = c1[:i] + c1[i+5:]
    return c1


def get_a(c):
    try:
        return BeautifulSoup(c, 'html5lib').a.string
    except AttributeError:
        if c.find('http://') != -1:
            return c[c.find('http://'):].split(' ')[0]
        else:
            return ''

# x1 = 'http://tieba.baidu.com/p/4260990232'
# x2 = get_all_floors(x1)
# for x3 in x2:
#     print('Floor #' + str(floor_get_floor_number(x3)))
#     print(floor_get_content(x3))
