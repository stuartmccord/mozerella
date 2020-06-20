from mozerella.parser import Parser


class TestParser:
    def test_get_domain(self):
        domain = Parser.get_domain('https://www.bbcgoodfood.com/recipes/cinnamon-rolls')
        assert domain == 'bbcgoodfood.com'

    def test_bbc_food(self, mocker):
        url = "https://www.bbcgoodfood.com/recipes/cinnamon-rolls"
        mock = mocker.patch('mozerella.parser.BBCGoodFoodParser.__init__', return_value=None)
        Parser.factory(url)
        mock.assert_called_once_with(url)


