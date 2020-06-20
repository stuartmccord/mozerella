import re


class Parser(object):

    @classmethod
    def factory(self, url):
        domain = self.get_domain(url)
        if domain == 'bbcgoodfood.com':
            return BBCGoodFoodParser(url)

    @classmethod
    def get_domain(self, url):
        extract_domain_pattern = "(?:(?:https?|ftp)://)?(?:www\.)?([^/\r\n]+)(?:/[^\r\n]*)?"
        return re.search(extract_domain_pattern, url).groups()[0]


class BBCGoodFoodParser(Parser):

    def __init__(self, url):
        self.url = url
