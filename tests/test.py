# arbituary testing code
import unittest
import snirf2bids as s2b
import os
import sys
import numpy as np
import shutil
import time
import json

data_directory = os.path.join('tests', 'data')  # Sample data source
working_directory = os.path.join('tests', 'temp')

if not os.path.isdir(working_directory):
    os.mkdir(working_directory)

if len(os.listdir(data_directory)) == 0:
    sys.exit('Failed to find test data in '+data_directory)

class FakeTest(unittest.TestCase):

    def test_json_output(self):
        # create subject
        subj1 = s2b.Subject(fpath=self._test_files[1])
        jsontext = subj1.json_export()
        temp = json.load(jsontext)

        # load standard data
        reference = json.load(self._test_files[0])

        self.assert_(sorted(temp.items()) == sorted(reference.items()))

    def setUp(self):
        print('Copying all test files to', working_directory)
        for file in os.listdir(data_directory):
            shutil.copy(os.path.join(data_directory, file), os.path.join(working_directory, file))
            time.sleep(0.5)  # Sleep while executing copy operation

        self._test_files = [working_directory + '/' + file for file in os.listdir(working_directory)]
        if len(self._test_files) == 0:
            sys.exit('Failed to set up test data working directory at ' + working_directory)

    def tearDown(self):
        print('Deleting all files in', working_directory)
        for file in os.listdir(working_directory):
            os.remove(os.path.join(working_directory, file))
            print('Deleted', working_directory + '/' + file)

if __name__ == '__main__':
    result = unittest.main()

