from dataclasses import dataclass
import re

# @dataclass
class Sentiment:
    def __init__(self,text):
        self.text = text
        self.sent_list = []
        self.word_list = []
        self.weight = 0

        with open("good_words.txt",encoding="utf-8") as f:
            self.positive_words = set(word for word in f.read().split('\n'))

        with open("bad_words.txt", encoding="utf-8") as f:
            self.negative_words = set(word for word in f.read().split('\n'))
        self.sentence_tokenize()
        self.word_tokenize()
        self.weight_count()


    def sentence_tokenize(self):
        sentence_pattern = re.compile(r'(.*?\.)(\s|$)', re.DOTALL)
        matches = sentence_pattern.findall(self.text) 
        self.sent_list = [match[0] for match in matches]
        

    def word_tokenize(self):
        word_pattern = re.compile(r"([\w\-']+)([\s,.])?")  
        for sentence in self.sent_list:
            matches = word_pattern.findall(sentence)
            self.word_list.extend([match[0] for match in matches])        

    def weight_count(self):
        for word in self.word_list:
            if word in self.positive_words:
                self.weight += 1
            if word in self.negative_words:
                self.weight -= 1


if __name__ == '__main__':

    review = '''Great neck, great fretwork, 
                great finish, great craftsmanship, 
                and a great tremolo. 
                New pickups make it sing, good sustain as well. 
                This is the best guitar under 
                $750 (the price of my Fender Strat Floyd Rose).'''

    test = Sentiment(text=review)
    # print(test.text)
    # print(test.sent_list)
    # print(test.word_list)
    print(test.weight)
