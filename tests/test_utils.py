import unittest
import collections

from hl7.xml import utils


class Model(object):
    pass


class UtilsTestCase(unittest.TestCase):
    def test_isinstance_all(self):
        self.assertTrue(utils.isinstance_all([1, 2, 3, 4], int))
        self.assertTrue(utils.isinstance_all(['Hello', 20], (str, int)))
        self.assertTrue(utils.isinstance_all([Model(), Model()], Model))    

        self.assertFalse(utils.isinstance_all([1, 2, 3], str))
        self.assertFalse(utils.isinstance_all([1, 2, False], bool))
        self.assertFalse(utils.isinstance_all([Model(), Model()], (str, bytes)))

        self.assertRaises(Exception, utils.isinstance_all, iterable=Model(), class_or_tuple=Model)
    
    def test_iter_without(self):
        self.assertEqual(utils.iter_without([1, None, 10, 100, None]), [1, 10, 100])
        self.assertEqual(utils.iter_without([1, 2, 3, 1, 2, 3], 2), [1, 3, 1, 3])
    
    def test_len_without(self):
        self.assertEqual(utils.len_without([1, None, 10, 100, None]), 3)
        self.assertEqual(utils.len_without([1, 2, 3, 1, 2, 3], 2), 4)
    
    def test_is_matrix(self):
        self.assertTrue(utils.is_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        self.assertTrue(utils.is_matrix(((1, 2), (4, 5), (7, 8, 8))))
        
        self.assertFalse(utils.is_matrix([1, 2, 3]))
        self.assertFalse(utils.is_matrix(((1, 2), 6, (7, 8, 8))))
    
    def test_flatten_matrix(self):
        self.assertEqual(
            list(utils.flatten_matrix([[1, 2], [[4, 5], [6, 7]]])), 
            [[1, 2], [4, 5], [6, 7]]
        )