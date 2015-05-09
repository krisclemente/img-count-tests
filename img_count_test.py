import unittest
import json
import requests
import sys, getopt

class ImageCountTestCases(unittest.TestCase):

    IMG_COUNT_FILE = 'img_count_output.txt'

    @classmethod
    def setUpClass(self):
        try:
            file = open(self.IMG_COUNT_FILE)
        except Exception, e:
            print e
            sys.exit(2)
        try:
            self.json_dict = json.loads(file.read())
        except ValueError, e:
            print self.IMG_COUNT_FILE + " is not valid JSON!"
            print e
            sys.exit(2)
        file.close()

    def testOutputIsAListOfDicts(self):
        """
            Description:    Test to ensure we have a list at the highest level and dictionaries at the second level
            Details:    Assert that self.json_dict is a list.
                        Assert that every element of self.json_dict is a dictionary
        """
        self.assertTrue(isinstance(self.json_dict,list))
        non_dicts = []
        for el in self.json_dict:
            if not isinstance(el,dict):
                non_dicts.append(el)
        self.assertFalse(non_dicts,
                            msg="The following elements in the list are not dictionaries:\n" + str(non_dicts))

    def testJsonKeys(self):
        """
            Description:    Test to ensure that all required keys and value types exist in each JSON block.
            Details:    Loops through each entry and checks to see if url, count and imdb_id is in the keys.
                        Also checks to see that each JSON has exactly 3 entries.
                        Test fails if any of the entries do not meet above criteria.
        """
        json_with_incorrect_keys = []
        correct_keys = [
            'url',
            'count',
            'imdb_id'
        ]
        for el in self.json_dict:
            if len(el) != 3:
                json_with_incorrect_keys.append(el)
            else:
                for key in correct_keys:
                    if key not in el:
                        json_with_incorrect_keys.append(el)
        self.assertFalse(json_with_incorrect_keys,
                            msg="The following dictionaries did not have the correct keys:\n" + str(json_with_incorrect_keys))

    def testJsonValueTypes(self):
        """
            Description:    Validate value types in json.
            Details:    Checks each entry and ensures 'url' and 'imdb_id' fields are strings and 'count' is an integer.
        """
        json_with_incorrect_values = [] 
        for el in self.json_dict:
            if not isinstance(el['url'],unicode):
                json_with_incorrect_values.append(el)
            if not isinstance(el['imdb_id'],unicode):
                json_with_incorrect_values.append(el)
            if not isinstance(el['count'],int):
                print "count mismatch:" + str(type(el['url']))
                json_with_incorrect_value.append(el)
        self.assertFalse(json_with_incorrect_values,
                            msg="The following dictionaries did not have the correct value type:\n" + str(json_with_incorrect_values))

    def testImdbIdInURL(self):
        """
            Description:    Test to ensure that IMDB ID is in the imdb url
            Details:    Assumes that imdb url is in the format "http://www.imdb.com/title/tt<imdb_id>"
                        Loops through all entries in IMG_COUNT_FILE and check if imdb_id is in the url.
                        If there are any, the test will fail.
        """
        imdb_id_url_mismatches = []
        for el in self.json_dict:
            if ('imdb_id' not in el) or ('url' not in el):
                imdb_id_url_mismatches.append(el)
            elif 'http://www.imdb.com/title/tt' + el['imdb_id'] != el['url']:
                imdb_id_url_mismatches.append(el)
        self.assertFalse(imdb_id_url_mismatches,
                            "The following dictionaries had a mismatch between the url and imdb_id:\n" + str(imdb_id_url_mismatches))

    def testAtLeastOneImageForEachJson(self):
        """
            Description:    Checks to see if each count > 0
            Details:    Assumes that each imdb url should return at least 1 image
                        Will loop through all entries and report back all entries that are not above 0
                        If any, the test will fail.
        """
        below_zero_elements = []
        for el in self.json_dict:
            if el['count'] < 0:
                below_zero_elements.append(el)
        self.assertFalse(below_zero_elements,
                            msg="The following dicationaries had counts below 0:\n" + str(below_zero_elements))

    def testValidImdbUrl(self):
        """
            Description:    Checks to see if each imdb url is valid and resolves
            Details:    Performs a GET on all IMDB urls.
                        Collects all urls that do not respond with a 200 return code.
                        If any, the test will fail. 
        """
        non_valid_urls = []
        for el in self.json_dict:
            response = requests.get(el['url'])
            if response.status_code != 200:
                non_valid_urls.append(el)
        self.assertFalse(non_valid_urls,
                            msg="The following dictionaries had urls that did not return 200s:\n" + str(non_valid_urls))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ImageCountTestCases.IMG_COUNT_FILE = sys.argv.pop()
    unittest.main()
