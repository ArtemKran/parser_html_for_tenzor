#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request as urllib
from bs4 import BeautifulSoup
import os
import configparser
import itertools
import re

__author__ = 'Artem Kraynev'

# КОНФИГИ
cfg = configparser.ConfigParser()
filename = 'config.yaml'
with open(filename) as fp:
    cfg.read_file(
        itertools.chain(['[global]'], fp),
        source=filename
    )
config_list = cfg.items('global')

PROXY = config_list[0][1]
HTTP_PROXY = config_list[1][1]
HTTPS_PROXY = config_list[2][1]
FTP_PROXY = config_list[3][1]


class Parser(object):

    def __init__(self, url):
        self.url = url
        self.url_is_valid = False
        self.html_text = None
        self.result = None
        self.validation_url()
        self.get_html_text()
        self.get_normal_text()
        self.write_to_file()

    def validation_url(self):
        """
        Проверяет на коректность введенный url
        :return: url_is_valid
        """
        url = self.url
        raw_result = re.match(r'(?:http)s?://', url)
        if raw_result is not None:
            self.url_is_valid = True
            return self.url_is_valid
        else:
            raise ValueError('Некоректный url')

    def get_html_text(self):
        """
        Парсит html текст, возвращает все теги
        <p> вместе с контентом
        :return: html_text
        """
        if self.url_is_valid:
            if PROXY == 'True':
                proxy_support = urllib.ProxyHandler(
                    {
                        'http': HTTP_PROXY,
                        'https': HTTPS_PROXY
                    }
                )
                opener = urllib.build_opener(proxy_support)
                urllib.install_opener(opener)
            html = urllib.urlopen(self.url).read()
            soup = BeautifulSoup(html, 'html.parser')
            self.html_text = soup.find_all('p')
            return self.html_text

    def get_normal_text(self):
        """
        Парсит html текст, возрашает контент,
        оборачивает ссылки в []
        :return: result
        """
        result_list = []
        for tag in self.html_text:
            if len(tag.contents) > 1:
                for content in tag.contents:
                    try:
                        attrs = getattr(content, 'attrs')
                        text = getattr(content, 'text')
                        result_list.append(
                            '[' + attrs['href'] + ']' + ' ' + text
                        )
                    except:
                        result_list.append(str(content))
            else:
                result_list.append('    ' + str(tag.contents[0]))
                result_list.append('\n\n')

        self.result = ' '.join(result_list)
        return self.result

    def write_to_file(self):
        """
        Записывает текст в файл
        """
        sub_list = [
            'http://',
            'https://',
            'www.'
        ]
        raw_path = self.url
        for sub in sub_list:
            path = raw_path.replace(sub, '')
            if len(path) < len(raw_path):
                break
        try:
            os.makedirs(path, 0o755)
            os.chdir(path)
        except FileExistsError:
            os.chdir(path)
        with open('post.odt', 'w') as f:
            f.write(self.result)

