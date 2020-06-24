import re
import urllib3
from bs4 import BeautifulSoup


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

    def __init__(self, url):
        self.url = url
        self.document = self.get_document()

    def get_document(self):
        http = urllib3.PoolManager()
        return http.urlopen(self.url)


class BBCGoodFoodParser(Parser):
    class Ingredient(object):
        def __init__(self, raw):
            self.raw = raw
            self.amount, self.unit, self.ingredient = re.match(r'(?:^(¼|½|¾|[0-9]*) ?(g|tbsp|tsp|ml)?) (.*)', self.raw).groups()

        def to_dict(self):
            return {
                'raw': self.raw,
                'amount': self.amount,
                'unit': self.unit,
                'ingredient': self.ingredient
            }

    def __init__(self, url):
        super().__init__(url)
        self.parser_engine = None

    def get_parser_engine(self):
        if self.parser_engine:
            return self.parser_engine

        return BeautifulSoup(self.document, 'html.parser')

    def get_title(self):
        return self.get_parser_engine().select('h1.recipe-header__title')[0].get_text()

    def get_description(self):
        return self.get_parser_engine().select('.recipe-header__description p')[0].get_text()

    def get_prep_time(self):
        return self.get_parser_engine().select('.recipe-details__cooking-time-prep .mins')[0].get_text()

    def get_cook_time(self):
        return self.get_parser_engine().select('.recipe-details__cooking-time-cook .mins')[0].get_text()

    def get_servings(self):
        return self.get_parser_engine().select('.recipe-details__item--servings .recipe-details__text')[0].get_text().rstrip().lstrip()

    def get_image(self):
        return self.get_parser_engine().select('.recipe-header .img-container img')[0]['src']

    def get_directions(self):
        method = self.get_parser_engine().select('#recipe-method ol.method__list li.method__item > p')
        return [item.get_text().lstrip().rstrip() for item in method]

    def get_ingredients(self):
        ingredients = self.get_parser_engine().select('.ingredients-list__content > *')
        groups = {}
        current_group = ""
        for ingredient in ingredients:
            if 'ingredients-list__group-title' in ingredient.attrs['class']:
                current_group = ingredient.get_text()
            if 'ingredients-list__group' in ingredient.attrs['class']:
                groups[current_group] = [
                    self.Ingredient(item.attrs['content']).to_dict()
                    for item in ingredient.find_all('li', class_='ingredients-list__item')
                ]
        return groups
