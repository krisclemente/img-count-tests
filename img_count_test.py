import unittest
import json
import requests
import sys

class ImageCountTestCases(unittest.TestCase):

    IMG_COUNT_FILE = 'img_count_output.txt'

    @classmethod
    def setUpClass(self):
        file = open(self.IMG_COUNT_FILE)
        try:
            self.json_dict = json.loads(file.read())
        except ValueError, e:
            print self.IMG_COUNT_FILE + " is not valid JSON!"
            print e
            sys.exit(2)
        file.close()

    def testJsonKeys(self):
        """
            Desciprtion:    Test to ensure that all required keys and only those key exist each JSON block.
            Details:    Loops through each entry and checks to see if url, count and imdb_id is in the keys.
                        Also checks to see that each JSON has exactly 3 entries.
        """
        incorrect_keys = []
        correct_keys = [
            'url',
            'count',
            'imdb_id'
        ]
        for el in self.json_dict:
            if len(el) != 3:
                incorrect_keys.append(el)
            else:
                for key in correct_keys:
                    if key not in el:
                        incorrect_keys.append(el)
        self.assertEquals(incorrect_keys,
                            [],
                            msg="The following dictionaries did not have the correct keys:\n" + str(incorrect_keys))

    def testImdbIdInURL(self):
        """
            Description:    Test to ensure that IMDB ID is in the imdb url
            Details:    Assumes that imdb url is in the format "http://www.imdb.com/title/tt<imdb_id>"
                        Loops through all entries in IMG_COUNT_FILE and check if imdb_id is in the url
        """
        imdb_id_url_mismatches = []
        for el in self.json_dict:
            if 'imdb_id' not in el:
                imdb_id_url_mismatches.append(el)
            elif 'http://www.imdb.com/title/tt' + el['imdb_id'] != el['url']:
                imdb_id_url_mismatches.append(el)
        self.assertEquals(imdb_id_url_mismatches,
                            [],
                            "The following dictionaries had a mismatch between the url and imdb_id:\n" + str(imdb_id_url_mismatches))

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
        self.assertEquals(below_zero_elements,
                            [],
                            msg="The following dicationaries had counts below 0:\n" + str(below_zero_elements))

    def testValidImdbUrl(self):
        """
            Description:    Checks to see if each imdb url is valid and resolves
            Details:    Performs a GET on all IMDB urls.
                        Collects all urls that do not respond with a 200 return code.
        """
        non_valid_urls = []
        for el in self.json_dict:
            response = requests.get(el['url'])
            if response.status_code != 200:
                non_valid_urls.append(el)
        self.assertEquals(non_valid_urls,
                            [],
                            msg="The following dictionaries had urls that did not return 200s:\n" + str(non_valid_urls))

if __name__ == '__main__':
    unittest.main()
