import requests
from bs4 import BeautifulSoup as Bs
from urllib.parse import urlparse


class Uri(object):
    PREFIX_WITH_URL = "%s%s"
    EMPTY_STRING = ""

    def __init__(self, url):
        self.url = url
        self.images = []
        self.links = []
        self.net_loc = get_urlparse_data(url).netloc
        self.scheme = get_urlparse_data(url).scheme
        if not self.net_loc.startswith("www") and self.net_loc.count(".") != 2:
            self.url = "%s://www.%s" % (get_urlparse_data(self.url).scheme, get_urlparse_data(self.url).netloc)

    def add_link(self, link):
        self.links.extend([link])

    def add_images(self, link):
        self.images.extend([link])

    def get_soup(self, verify=False):
        """

        :param verify: to verify ssl or not
        :return: BeautifulSoup object
        """
        return Bs(self.get_uri_content(verify=verify), features="html5lib")

    @property
    def get_all_links(self):
        try:
            return set(map(get_href, self.get_soup().find_all('a', href=True)))
        except Exception as e:
            print(e)
            return []

    @property
    def get_all_images(self):
        try:
            return set(map(get_src, self.get_soup().find_all('img')))
        except Exception as e:
            print(e)
            return []

    def get_uri_content(self, verify=False):
        r = requests.get(self.url, verify=verify)
        return r.content

    def filter_related_links(self, link):
        """

        :param link: url link to filter
        """
        if not link.startswith("//") and link.startswith("/") or self.net_loc in get_urlparse_data(link).netloc:
            return True
        else:
            return False

    def get_all_relative_links(self):
        s = []
        filtered_links = filter(self.filter_related_links, self.get_all_links)
        filtered_images = self.get_all_images
        for link in filtered_links:
            if link.startswith("/"):
                self.add_link(Uri(self.PREFIX_WITH_URL % (self.url, link)))
            else:
                self.add_link(Uri(link))

        for link in filtered_images:
            if not link.startswith("//") and link.startswith("/") or self.net_loc in get_urlparse_data(link).netloc:
                self.add_images(self.PREFIX_WITH_URL % (self.url, link))
            else:
                self.add_images(link)
        return self


def get_urlparse_data(link):
    return urlparse(link)


def get_href(link):
    return link['href']


def get_src(link):
    return link["src"]
