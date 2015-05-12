import unittest
import json
import sys
import os
import subprocess
import time

class ImageCountTestCases(unittest.TestCase):

    IMG_COUNT_PATH = 'img_count.py'

    @classmethod
    def setUpClass(self):
        self.start = time.time() 
        proc = subprocess.Popen(['python',self.IMG_COUNT_PATH], stdout=subprocess.PIPE)
        self.end = time.time() 
        output = proc.stdout.read()
        try:
            self.json_dict = json.loads(output)
        except ValueError, e:
            print self.IMG_COUNT_PATH + " did not output valid JSON!"
            print e
            sys.exit(2)

    def testRunUnderEightSeconds(self):
        """
            Description:    Test to check if img_count.py runs under 8 seconds
            Details:    Uses self.start and self.end, captured in the setUpClass
        """
        self.assertTrue((self.end - self.start) < 8)

    def testOutputIsAList(self):
        """
            Description:    Test to ensure we have a list at the highest level
            Details:    Assert that self.json_dict is a list.
        """
        self.assertTrue(isinstance(self.json_dict,list))

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
            Details:    Checks each entry and ensures 'url' and 'imdb_id' fields are unicode and 'count' is an integer.
        """
        json_with_incorrect_values = []
        incorrect_values_list = []
        for el in self.json_dict:
            incorrect_values = []
            if 'url' in el and not isinstance(el['url'],unicode):
                incorrect_values.append({el['url']:str(type(el['url'])) + " and needs to be unicode"})
            if 'imdb_id' in el and not isinstance(el['imdb_id'],unicode):
                incorrect_values.append({el['imdb_id']:str(type(el['imdb_id'])) + " and needs to be unicode"})
            if 'count' in el and not isinstance(el['count'],int):
                incorrect_values.append({el['count']:str(type(el['count'])) + " and needs to be int"})
            if incorrect_values:
                json_with_incorrect_values.append(el)
                incorrect_values_list.append(incorrect_values)
        self.assertFalse(json_with_incorrect_values,
                            msg="The following dictionaries did not have a correct value type:" + str(json_with_incorrect_values) +
                            "\nDict of incorrect values:" + str(incorrect_values_list))

    def testImdbURLFormat(self):
        """
            Description:    Test to ensure that IMDB ID is in the imdb url and is in the proper format.
            Details:    Assumes that imdb url is in the format "http://www.imdb.com/title/tt<imdb_id>".
                        Loops through all entries in IMG_COUNT_FILE and check if imdb_id is in the url.
        """
        imdb_id_url_mismatches = []
        for el in self.json_dict:
            if ('imdb_id' not in el) or ('url' not in el):
                imdb_id_url_mismatches.append(el)
            elif 'http://www.imdb.com/title/tt' + str(el['imdb_id']) != el['url']:
                imdb_id_url_mismatches.append(el)
        self.assertFalse(imdb_id_url_mismatches,
                            msg="The following dictionaries had improperly formatted IMDB urls\n" + str(imdb_id_url_mismatches))

    def testAtLeastOneImageForEachJson(self):
        """
            Description:    Checks to see if each count > 0
            Details:    Assumes that each imdb url should return at least 0 images
                        Will loop through all entries and report back all entries that below 0
                        If any, the test will fail.
        """
        below_zero_elements = []
        for el in self.json_dict:
            if el['count'] < 0:
                below_zero_elements.append(el)
        self.assertFalse(below_zero_elements,
                            msg="The following dicationaries had counts below 0:\n" + str(below_zero_elements))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ImageCountTestCases.IMG_COUNT_PATH = sys.argv.pop()
    unittest.main()
