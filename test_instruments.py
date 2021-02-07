import unittest, sqlite3
import instruments

class Test_Instruments(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        source = sqlite3.connect('music_store.db')
        dest = sqlite3.connect(':memory:')
        source.backup(dest)
        
        cls.instr = instruments.Instrument(ref=777777, db=':memory:')
        cls.review = instruments.Review(id="Kyle", ref='777777', stars="5", review="We need more cow bell", verified=True, sentiment= None)
        


    @classmethod
    def tearDownClass(cls):
        pass
    
    # def setUp(self):
    #     self.instr = instruments.Instrument(ref=777777)#, db=':memory:')
    #     self.review = instruments.Review(id="Kyle", ref='11111', stars="5", review="this is good stuff")

    # def tearDown(self):
    #     pass

    def test_Instruments_init(self):
        self.assertEqual(self.instr.name, "Cow Bells")
        self.assertEqual(self.instr.cat, "percussion")

    def test_Reviews(self):
        import_review_list = instruments.
        print(import_review_list)
        self.assertEqual(self.review.to_dict(), import_review_list[0])
        pass
        
if __name__ == '__main__':
    unittest.main() 