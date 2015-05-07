import unittest
import json

class ImageCountTestCases(unittest.TestCase):

    IMG_COUNT_FILE = 'img_count_output.txt'

    def setUp(self):
        file = open(self.IMG_COUNT_FILE)
        self.json_dict = json.loads(file.read())
        file.close()

    def testImdbIdInURL(self):
        """
            Description:    Test to ensure that IMDB ID is in the imdb url
            Details:    Assumes that imdb url is in the format "http://www.imdb.com/title/tt<imdb_id>"
                        Loops through all entries in IMG_COUNT_FILE and check if imdb_id is in the url
        """
        imdb_id_url_mismatches = []
        for el in self.json_dict:
            if 'http://www.imdb.com/title/tt' + el['imdb_id'] != el['url']:
                imdb_id_url_mismatches.append(el)
        self.assertEquals(imdb_id_url_mismatches,[])

    def testAtLeastOneImageForEach(self):
        """
            Description:    Checks to see if each count > 0
            Details:    Assumes that each imdb url should return at least 1 image
                        Will loop through all entries and report back all entries that are not above 0
        """
        below_zero_elements = []
        for el in self.json_dict:
            if el['count'] < 1:
                below_zero_elements.append(el)
        self.assertEquals(below_zero_elements,[])
        
if __name__ == '__main__':
    unittest.main()
