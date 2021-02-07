import unittest
import sqlite3
from sentiment import Sentiment

class test_Sentiment(unittest.TestCase):

    def setUp(self):
        review = '''Great neck, great fretwork, 
                    great finish, great craftsmanship, 
                    and a great tremolo. 
                    New pickups make it sing, good sustain as well. 
                    This is the best guitar under 
                    $750 (the price of my Fender Strat Floyd Rose).'''

        self.text = review
        self.instance = Sentiment(text=self.text)

    def test_sent(self):
        self.assertEqual(self.instance.weight, 7)
        
if __name__ == '__main__':
    unittest.main()