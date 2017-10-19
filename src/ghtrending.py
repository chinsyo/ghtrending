# coding: utf-8

__author__ = 'Chinsyo'
__version__ = '0.0.2'

import sys
import time
import argparse

import requests
from lxml import etree

if sys.version > '3':
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

GHTRENDING_ROOT_URL = 'http://github.com/trending/'
GHTRENDING_SINCE = {'today', 'weekly', 'monthly'}
GHTRENDING_QTYPE = ['', 'developers/']

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}


def _print_sectiontitle(title):
    print('=' * 60)
    print(time.strftime('%Y-%m-%d', time.localtime()), title)
    print('=' * 60)


def _print_separateline():
    print('-' * 60)


def _xpath_firstornull(tags):
    return tags[-1] if len(tags) else '<null>'


def _gettrending_repository(html):
    repo_list = html.xpath('//ol[@class="repo-list"]/li')
    _print_sectiontitle('Top {} Github Trending Repository'.format(len(repo_list)))

    for index, repo in enumerate(repo_list):
        today = _xpath_firstornull(repo.xpath('.//svg[@class="octicon octicon-star"]/parent::node()/text()'))
        name = _xpath_firstornull(repo.xpath('.//div[contains(@class, "col-9")]/h3/a/@href'))
        desc = _xpath_firstornull(repo.xpath('.//div[@class="py-1"]/p/text()'))
        star = _xpath_firstornull(repo.xpath('.//svg[contains(@aria-label, "star")]/parent::node()/text()'))
        fork = _xpath_firstornull(repo.xpath('.//svg[contains(@aria-label, "fork")]/parent::node()/text()'))

        _print_separateline()
        print("* No.{} {} ({})".format(index + 1, name.strip()[1:], today.strip()))
        print("* star: {} \tfork: {}".format(star.strip(), fork.strip()))
        print("* desc: {}".format(desc.strip()))
    _print_separateline()


def _gettrending_developers(html):
    developers = html.xpath('//ol[@class="list-style-none"]/li')
    _print_sectiontitle('Top {} Github Trending Developers'.format(len(developers)))

    for index, developer in enumerate(developers):
        _print_separateline()
        name = developer.xpath('.//div[@class="mx-2"]/h2/a/text()')[0]
        repo = _xpath_firstornull(developer.xpath('.//span[contains(@class, "repo-snipit-name")]/span/text()'))
        desc = _xpath_firstornull(developer.xpath('.//span[contains(@class, "repo-snipit-description")]/text()'))
        print('* No.{} {}'.format(index + 1, name.strip()))
        print('* repo: {}'.format(repo.strip()))
        print('* desc: {}'.format(desc.strip()))
    _print_separateline()


def main():
    args = ARGS.parse_args()
    assert args.qtype < len(GHTRENDING_QTYPE)
    assert args.since in GHTRENDING_SINCE

    params = {'since': args.since} if (args.since is not 'today') else None

    url = GHTRENDING_ROOT_URL
    url = urljoin(url, GHTRENDING_QTYPE[args.qtype])
    url = urljoin(url, args.lang)

    request = requests.get(url, headers=headers, params=params)
    request.encoding = 'utf-8'
    assert request.status_code == 200

    html = etree.HTML(request.text)
    if args.qtype == 0:
        _gettrending_repository(html)
    else:
        _gettrending_developers(html)


ARGS = argparse.ArgumentParser(description='Github Trending')
ARGS.add_argument('-q', '--qtype', dest='qtype', default=0, action='store', type=int,
                  help='Setting the query type, 0 for repository, 1 for developers')
ARGS.add_argument('-s', '--since', dest='since', default='today', action='store', type=str,
                  help='Setting the since today/weekly/monthly')
ARGS.add_argument('-l', '--lang', dest='lang', action='store', type=str, help='Specity language')
if __name__ == '__main__':
    main()
