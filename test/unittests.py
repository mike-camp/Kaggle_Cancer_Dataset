
'''Unit Tests for preprocessing functions
To run the tests: go to the root directory, Kaggle-Cancer-Dataset
run `make test`
'''
from __future__ import division
import unittest as unittest
import numpy as np
from src import preprocessing


class TestPreprocessing(unittest.TestCase):

    def test_remove_fig(self):
        result = preprocessing.clean_text("From fig. 1 we see")
        self.assertEqual(result,"from  we see")

    def test_remove_figure(self):
        result = preprocessing.clean_text("see Figure A")
        self.assertEqual(result,"see")

    def test_remove_number(self):
        result = preprocessing.clean_text("the result increased by 22.7%")
        self.assertEqual(result,"the result increased by")

    def test_remove_number_comma(self):
        result = preprocessing.clean_text("the numbers range from 1,2,3")
        self.assertEqual(result,"the numbers range from")

    def test_dont_remove_gene(self):
        result = preprocessing.clean_text("the gene WK320 is associated with")
        self.assertEqual(result,"the gene wk320 is associated with")

    def test_remove_letter_reference(self):
        result = preprocessing.clean_text("from [a] we see that [B] should")
        self.assertEqual(result,"from  we see that  should")
