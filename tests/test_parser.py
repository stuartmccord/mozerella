from mozerella.parser import Parser, BBCGoodFoodParser
import pytest
import os


class TestParser:
    def test_get_domain(self, bbc_good_food_url):
        domain = Parser.get_domain(bbc_good_food_url)
        assert domain == 'bbcgoodfood.com'

    def test_get_document(self, mocker, bbc_good_food_url):
        mock_requests_get = mocker.patch('urllib3.PoolManager.urlopen', return_value="<html></html>")
        Parser.factory(bbc_good_food_url)

        mock_requests_get.assert_called_once_with(bbc_good_food_url)

    def test_bbc_food(self, mocker, bbc_good_food_url):
        mock_init = mocker.patch('mozerella.parser.BBCGoodFoodParser.__init__', return_value=None)
        Parser.factory(bbc_good_food_url)

        mock_init.assert_called_once_with(bbc_good_food_url)


class TestBBCGoodFoodParser:
    def test_it_parses_the_document(self, bbc_good_food_parser):
        assert bbc_good_food_parser.get_title() == "Cinnamon rolls"
        assert bbc_good_food_parser.get_description() == "Try these easy cinnamon rolls with vanilla icing as a treat for afternoon tea. They're delicious served warm or cold – you can also make them ahead and freeze"
        assert bbc_good_food_parser.get_prep_time() == "40 mins"
        assert bbc_good_food_parser.get_cook_time() == "35 mins"
        assert bbc_good_food_parser.get_servings() == 'Makes 8'
        assert bbc_good_food_parser.get_image() == '//www.bbcgoodfood.com/sites/default/files/styles/recipe/public/recipe/recipe-image/2018/06/cinnamon-buns.jpg?itok=N8YEo0yS'

    def test_it_parses_the_directions(self, bbc_good_food_parser):
        directions = bbc_good_food_parser.get_directions()
        assert len(directions) == 3
        assert "Heat oven to 180C/fan 160C/gas 4." in directions[0]
        assert "Mix the filling ingredients together." in directions[1]
        assert "Sift the icing sugar into a large bowl" in directions[2]

    def test_it_parses_the_ingredients(self, bbc_good_food_parser):
        ingredient_containers = bbc_good_food_parser.get_ingredients()
        fillings = ingredient_containers['For the filling']
        assert len(ingredient_containers) == 3
        assert '' in ingredient_containers
        assert 'For the filling' in ingredient_containers
        assert 'For the icing' in ingredient_containers
        assert len(fillings) == 4
        assert '1 tsp ground cinnamon' in fillings
        assert '55g light brown soft sugar' in fillings
        assert '2 tbsp caster sugar' in fillings
        assert '40g butter, melted' in fillings



@pytest.fixture
def bbc_good_food_parser(bbc_good_food_document, bbc_good_food_url, mocker):
    mocker.patch('mozerella.parser.BBCGoodFoodParser.get_document', return_value=bbc_good_food_document)
    parser = BBCGoodFoodParser(bbc_good_food_url)
    return parser


@pytest.fixture
def bbc_good_food_url():
    return "https://www.bbcgoodfood.com/recipes/cinnamon-rolls"


@pytest.fixture
def bbc_good_food_document():
    dir = os.path.dirname(__file__)
    relative_file_path = "fixtures/bbcgoodfood.html"
    absolute_file_path = os.path.join(dir, relative_file_path)

    document = open(absolute_file_path, "r")
    return document.read()