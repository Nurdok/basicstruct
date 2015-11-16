from collections import OrderedDict

import six
import pickle
import unittest

from basicstruct import BasicStruct


class SimpleBasicStruct(BasicStruct):
    __slots__ = ('x', 'y')


class BasicStructWithUnorderedDefaultValues(BasicStruct):
    __slots__ = {'x': 5, 'y': True}


class BasicStructWithOrderedDefaultValues(BasicStruct):
    __slots__ = OrderedDict((('x', 5), ('y', True)))


class BasicStructTest(unittest.TestCase):
    def test_attribute_access(self):
        bs = SimpleBasicStruct(2, 'blah')
        self.assertEqual(bs.x, 2)
        self.assertEqual(bs.y, 'blah')

    def test_attribute_access_with_kwargs(self):
        bs = SimpleBasicStruct(x=2, y='blah')
        self.assertEqual(bs.x, 2)
        self.assertEqual(bs.y, 'blah')

    def test_attribute_access_partly_kwargs(self):
        bs = SimpleBasicStruct(2, y='blah')
        self.assertEqual(bs.x, 2)
        self.assertEqual(bs.y, 'blah')

    def test_attribute_access_missing_values(self):
        bs = SimpleBasicStruct(2)
        self.assertEqual(bs.x, 2)
        self.assertEqual(bs.y, None)

    def test_attribute_access_missing_values_partial_kwargs(self):
        bs = SimpleBasicStruct(y=2)
        self.assertEqual(bs.x, None)
        self.assertEqual(bs.y, 2)

    def test_comparisons(self):
        small = SimpleBasicStruct(1, 'irrelevant')
        medium = SimpleBasicStruct(2, 5)
        another_medium = SimpleBasicStruct(2, 5)
        large = SimpleBasicStruct(2, 15)

        self.assertEqual(medium, another_medium)

        self.assertTrue(small < medium)
        self.assertTrue(small < large)
        self.assertTrue(small <= medium)
        self.assertTrue(small <= large)
        self.assertTrue(medium < large)
        self.assertTrue(medium <= another_medium)
        self.assertTrue(another_medium <= medium)

        self.assertTrue(medium > small)
        self.assertTrue(large > small)
        self.assertTrue(medium >= small)
        self.assertTrue(large >= medium)
        self.assertTrue(large > medium)
        self.assertTrue(medium >= another_medium)
        self.assertTrue(another_medium >= medium)

        self.assertTrue(small != medium)
        self.assertTrue(medium != small)
        self.assertTrue(medium != large)
        self.assertTrue(large != medium)

        # need to call the magic method directly, otherwise the reverse
        # method is called, which is implemented in Python 2.x
        self.assertEqual(small.__gt__(1), NotImplemented)
        self.assertEqual(small.__ge__(1), NotImplemented)
        self.assertEqual(small.__lt__(1), NotImplemented)
        self.assertEqual(small.__le__(1), NotImplemented)
        self.assertEqual(small.__eq__(1), NotImplemented)
        self.assertEqual(small.__ne__(1), NotImplemented)

        if six.PY3:
            with self.assertRaises(TypeError):
                small < 1

            with self.assertRaises(TypeError):
                small <= 1

            with self.assertRaises(TypeError):
                small > 1

            with self.assertRaises(TypeError):
                small >= 1

    def test_repr(self):
        bs = SimpleBasicStruct(1, 'irrelevant')
        self.assertEqual(repr(bs), "SimpleBasicStruct(x=1, y='irrelevant')")

    def test_pickle(self):
        bs = SimpleBasicStruct(1, 'irrelevant')
        self.assertEqual(bs, pickle.loads(pickle.dumps(bs)))

    def test_hash(self):
        small = SimpleBasicStruct(1, 'irrelevant')
        medium = SimpleBasicStruct(2, 5)
        another_medium = SimpleBasicStruct(2, 5)
        large = SimpleBasicStruct(2, 15)

        self.assertNotEqual(hash(small), hash(medium))
        self.assertNotEqual(hash(medium), hash(large))
        self.assertEqual(hash(medium), hash(another_medium))

    def test_to_dict(self):
        bs = SimpleBasicStruct(1, 2)
        d1 = bs.to_dict()
        d2 = dict(bs)
        expected = {'x': 1, 'y': 2}

        self.assertEqual(d1, expected)
        self.assertEqual(d2, expected)

    def test_to_dict_copy(self):
        l = []
        bs = SimpleBasicStruct(1, l)
        d1 = bs.to_dict()
        d2 = bs.to_dict(copy=True)
        l.append(1)

        self.assertEqual(d1, {'x': 1, 'y': [1]})
        self.assertEqual(d2, {'x': 1, 'y': []})

    def test_unordered_default_values(self):
        bs = BasicStructWithUnorderedDefaultValues()
        self.assertEqual(bs.x, 5)
        self.assertEqual(bs.y, True)

    def test_unordered_partial_default_values_keyword_args(self):
        bs = BasicStructWithUnorderedDefaultValues(x=0)
        self.assertEqual(bs.x, 0)
        self.assertEqual(bs.y, True)

    def test_unordered_default_values_non_keyword_arg(self):
        with self.assertRaises(ValueError):
            BasicStructWithUnorderedDefaultValues(0)

        with self.assertRaises(ValueError):
            BasicStructWithUnorderedDefaultValues(False, x=0)

    def test_ordered_default_values(self):
        bs = BasicStructWithOrderedDefaultValues()
        self.assertEqual(bs.x, 5)
        self.assertEqual(bs.y, True)

    def test_ordered_partial_default_values_keyword_args(self):
        bs = BasicStructWithOrderedDefaultValues(x=0)
        self.assertEqual(bs.x, 0)
        self.assertEqual(bs.y, True)

    def test_ordered_partial_default_values(self):
        bs = BasicStructWithOrderedDefaultValues(0)
        self.assertEqual(bs.x, 0)
        self.assertEqual(bs.y, True)

    def test_ordered_partial_default_values_with_kwargs(self):
        bs = BasicStructWithOrderedDefaultValues(y=False)
        self.assertEqual(bs.x, 5)
        self.assertEqual(bs.y, False)


if __name__ == '__main__':
    unittest.main()

