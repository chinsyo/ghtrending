# coding: utf-8

import sys
import time
import json
import argparse

import requests
from lxml import etree
from json import JSONEncoder

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
    _print_separateline('=')
    print(time.strftime('%Y-%m-%d', time.localtime()), title)
    _print_separateline('=')


def _print_separateline(separator='-'):
    print(separator * 60)


def _xpath_textornull(el, stmt):
    tags = el.xpath(stmt)
    return tags[-1] if len(tags) else '<null>'

class GHEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class GHRepo(object):
    def __init__(self, html):
        self.today = _xpath_textornull(html, './/svg[@class="octicon octicon-star"]/parent::node()/text()').strip()
        self.name = _xpath_textornull(html, './/div[contains(@class, "col-9")]/h3/a/@href').strip()
        self.desc = _xpath_textornull(html, './/div[@class="py-1"]/p/text()').strip()
        self.star = _xpath_textornull(html, './/svg[contains(@aria-label, "star")]/parent::node()/text()').strip()
        self.fork = _xpath_textornull(html, './/svg[contains(@aria-label, "fork")]/parent::node()/text()').strip()

    def __str__(self):
        description = ""
        description += "* 🌍 No.{} {} ({})".format(self.index, self.name[1:], self.today)
        description += "\n"
        description += "* 🌟 star: {} \t🍴 fork: {}".format(self.star, self.fork)
        description += "\n"
        description += "* 📚 desc: {}".format(self.desc)
        return description

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, v):
        self._index = v if v >= 0 else 0


class GHUser(object):
    def __init__(self, html):
        self.name = html.xpath('.//div[@class="mx-2"]/h2/a/text()')[0].strip()
        self.repo = _xpath_textornull(html, './/span[contains(@class, "repo-snipit-name")]/span/text()').strip()
        self.desc = _xpath_textornull(html, './/span[contains(@class, "repo-snipit-description")]/text()').strip()

    def __str__(self):
        description = ""
        description += "* 🌍 No.{} {}".format(self.index, self.name)
        description += "\n"
        description += "* 📦 repo: {}".format(self.repo)
        description += "\n"
        description += "* 📚 desc: {}".format(self.desc)
        return description

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, v):
        self._index = v if v >= 0 else 0


class GHClient(object):
    def __init__(self, qtype=0, since='today', lang=None, json=False):
        self.qtype = qtype
        self.since = since
        self.lang = lang
        self.json = json

    def request(self):
        html = self._getcontent()
        if self.qtype == 0:
            self._parse_trending_repository(html)
        else:
            self._parse_trending_developers(html)

    def _getcontent(self):
        assert self.qtype < len(GHTRENDING_QTYPE)
        assert self.since in GHTRENDING_SINCE

        params = {'since': self.since} if (self.since is not 'today') else None

        url = GHTRENDING_ROOT_URL
        url = urljoin(url, GHTRENDING_QTYPE[self.qtype])
        url = urljoin(url, self.lang)

        request = requests.get(url, headers=headers, params=params)
        request.encoding = 'utf-8'
        assert request.status_code == 200

        html = etree.HTML(request.text)
        return html

    def _parse_trending_repository(self, html):
        repo_list = html.xpath('//ol[@class="repo-list"]/li')
        _print_sectiontitle('Top {} Github Trending Repository'.format(len(repo_list)))

        repos = []
        for index, repo in enumerate(repo_list):
            r = GHRepo(repo)
            r.index = index + 1
            if self.json:
                repos.append(r)
            else:
                _print_separateline()
                print(r)

        if self.json:
            print(json.dumps(repos, cls=GHEncoder, indent=4))
            

    def _parse_trending_developers(self, html):
        developers = html.xpath('//ol[@class="list-style-none"]/li')
        _print_sectiontitle('Top {} Github Trending Developers'.format(len(developers)))
        
        users = []
        for index, developer in enumerate(developers):
            u = GHUser(developer)
            u.index = index + 1
            if self.json:
                users.append(u)
            else:
                _print_separateline()
                print(u)

        if self.json:
            print(json.dumps(users, cls=GHEncoder, indent=4))


def main():
    args = ARGS.parse_args()
    GHClient(args.qtype, args.since, args.lang, args.json).request()


ARGS = argparse.ArgumentParser(description='Github Trending')
ARGS.add_argument('-q', '--qtype', dest='qtype', default=0, action='store', type=int,
                  help='Setting the query type, 0 for repository, 1 for developers')
ARGS.add_argument('-s', '--since', dest='since', default='today', action='store', type=str,
                  help='Setting the since today/weekly/monthly')
ARGS.add_argument('-l', '--lang', dest='lang', action='store', type=str, help='Specity language')
ARGS.add_argument('-j', '--json', dest='json', action='store_true', help='JSON output format')
ARGS.set_defaults(json=False)
if __name__ == '__main__':
    main()
    