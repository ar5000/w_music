import unittest, sqlite3
import instruments

class Test_Instruments(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # source = sqlite3.connect('music_store.db')
        # dest = sqlite3.connect('music_store1.db')
        # source.backup(dest)
        
        cls.instr = instruments.Instrument(ref=777777, db='music_store1.db')
        cls.review = instruments.Review(db='music_store1.db', id="Kyle", ref='777777', stars="5", review="We need much more cow bell", verified=True, sentiment= None)
        cls.review.post_review()


    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_Instruments_init(self):
        self.assertEqual(self.instr.name, "Cow Bells")
        self.assertEqual(self.instr.cat, "percussion")

    def test_Reviews(self):
        import_review_list = instruments.Review.get_last_review(ref=777777, db='music_store1.db')
        import_review_dict = {"ref":str(import_review_list[2]), "id":import_review_list[3], "stars":str(import_review_list[4]), "review":import_review_list[5], "verified":bool(import_review_list[6]), "sentiment":import_review_list[7]}
        self.assertEqual(self.review.to_dict(), import_review_dict)

    def test_html_scrub(self):
            
        pass
        

    # def cleanup_html(self):
    #     self.assert(self.review)

if __name__ == '__main__':
    unittest.main() 