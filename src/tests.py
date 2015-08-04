import pickle
import unittest

from basicstruct import BasicStruct


class Foo(BasicStruct):
    __slots__ = ('x', 'y')


class MyTestCase(unittest.TestCase):
    def test_attribute_access(self):
        f = Foo(2, 'blah')
        self.assertEqual(f.x, 2)
        self.assertEqual(f.y, 'blah')

    def test_attribute_access_with_kwargs(self):
        f = Foo(x=2, y='blah')
        self.assertEqual(f.x, 2)
        self.assertEqual(f.y, 'blah')

    def test_attribute_access_partly_kwargs(self):
        f = Foo(2, y='blah')
        self.assertEqual(f.x, 2)
        self.assertEqual(f.y, 'blah')

    def test_comparisons(self):
        small = Foo(1, 'irreleant')
        medium = Foo(2, 5)
        another_medium = Foo(2, 5)
        large = Foo(2, 15)

        self.assertEqual(medium, another_medium)

        self.assertLess(small, medium)
        self.assertLess(small, large)
        self.assertLessEqual(small, medium)
        self.assertLessEqual(small, large)
        self.assertLess(medium, large)
        self.assertLessEqual(medium, another_medium)
        self.assertLessEqual(another_medium, medium)

        self.assertGreater(medium, small)
        self.assertGreater(large, small)
        self.assertGreaterEqual(medium, small)
        self.assertGreaterEqual(large, medium)
        self.assertGreater(large, medium)
        self.assertGreaterEqual(medium, another_medium)
        self.assertGreaterEqual(another_medium, medium)

    def test_repr(self):
        f = Foo(1, 'irrelevant')
        self.assertEqual(repr(f), "Foo(x=1, y='irrelevant')")

    def test_pickle(self):
        f = Foo(1, 'irrelevant')
        self.assertEqual(f, pickle.loads(pickle.dumps(f)))


if __name__ == '__main__':
    unittest.main()
