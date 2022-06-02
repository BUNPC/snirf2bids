# arbituary testing code
import unittest
import snirf2bids as s2b
import os
import sys
import numpy as np
import shutil
import time
import json
import tabulate
import io
import csv

data_directory = os.path.join('tests', 'data')  # Sample data source
working_directory = os.path.join('tests', 'temp')

if not os.path.isdir(working_directory):
    os.mkdir(working_directory)

if len(os.listdir(data_directory)) == 0:
    sys.exit('Failed to find test data in ' + data_directory)

class snirf2bids_Test(unittest.TestCase):

    def test_gen_from_all(self):
        """Confirm that all test data can be parsed without error."""
        for file in os.listdir(working_directory):
            if file.endswith('.snirf'):
                print('Generating BIDS information for', os.path.join(working_directory, file) + '...')
                j = s2b.snirf2json(os.path.join(working_directory, file))
                self.assertTrue(len(j) > 0, msg='Generation failed for ' + file)
                s = json.loads(j)
                for fname in s.keys():
                    print('__________________________________________________')
                    print('Generated', fname)
                    if fname.endswith('.json'):
                        print(json.dumps(json.loads(s[fname]), indent=2))
                    elif fname.endswith('.tsv'):
                        rows = csv.reader(io.StringIO(s[fname]), delimiter='\t')
                        print(tabulate.tabulate(rows))
                print('__________________________________________________')

    def setUp(self):
        print('Copying all test files to', working_directory)
        for file in os.listdir(data_directory):
            shutil.copy(os.path.join(data_directory, file), os.path.join(working_directory, file))
            time.sleep(0.5)  # Sleep while executing copy operation

        self._test_files = [os.path.join(working_directory, file) for file in os.listdir(working_directory)]
        if len(self._test_files) == 0:
            sys.exit('Failed to set up test data working directory at ' + working_directory)

    def tearDown(self):
        print('Deleting all files in', working_directory)
        for file in os.listdir(working_directory):
            os.remove(os.path.join(working_directory, file))
            print('Deleted', os.path.join(working_directory, file))

if __name__ == '__main__':
    result = unittest.main()

