import unittest
import automata
import bisect


words = [x.strip().lower() for x in open('sowpods.txt')]
words.sort()


class Tests(unittest.TestCase):
    def test_food(self):
        m = Matcher(words)
        self.assertEqual(len((list(automata.find_all_matches('food', 1, m)))), 18)
        self.assertEqual(len((list(automata.find_all_matches('food', 2, m)))), 318)

    def test_hello(self):
        m = Matcher(words)
        self.assertEqual(len((list(automata.find_all_matches('hello', 1, m)))), 12)
        self.assertEqual(len((list(automata.find_all_matches('hello', 2, m)))), 128)

    def test_slice(self):
        m = Matcher(words)
        self.assertEqual(len((list(automata.find_all_matches('slice', 1, m)))), 15)
        self.assertEqual(len((list(automata.find_all_matches('slice', 2, m)))), 213)

class Matcher(object):
    def __init__(self, l):
        self.l = l
        self.probes = 0

    def __call__(self, w):
        self.probes += 1
        pos = bisect.bisect_left(self.l, w)
        if pos < len(self.l):
            return self.l[pos]
        else:
            return None

if __name__ == '__main__':
    unittest.main()
