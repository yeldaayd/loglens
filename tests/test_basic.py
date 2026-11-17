import unittest

class BasicTests(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(1 + 1, 2)

if _name_ == "_main_":
    unittest.main()
