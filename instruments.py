import sqlite3
conn = sqlite3.connect("music_store.db")
c = conn.cursor()
# [START models]
from database import instrument_model
def search_ref(ref):
    instrument_model.show_one(c, (ref,))
    _, name, _, _ = c.fetchone()
    return name

class Datastore:
    def __init__(self):

    def login(self, username, password):

    def logout(self):

    def connect(self, filename='music_store.db'):
        self.conn = sqlite3.connect(filename)
        self.cu = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def get_instrument(self, ref_num):
        cursor.execute("SELECT * FROM instruments WHERE ref_num= :ref", "ref":ref_num)
        return ???

    def setsomedatat(self, fields):
       cursor.execute("INSERT INTO instruments VALUES (?,?,?,?)", fields)
       return 


class Instrument:
    playable = True
    def __init__(self, category, name, ref, image, playable=True):
        self.category = category
        self.name = name
        self.ref = ref
        # self.playable = playable
        # self.played = 0
        self.image = image

    def __str__(self):
        return f"This is a {self.name} and is a {self.category} instrument"

    def __repr__(self):
        return f"Instrument({self.ref}, {self.name}, {self.category})"

    def fromtuple(self, fields):
        self.ref, self.name, self.category, self.image = fields

    def totuple(self):
        return (self.ref, self.name, self.category, self.image)

    def increase_play_count(self):
        self.played += 1

    @classmethod
    def non_playable(cls, category, name):
        return cls(category, name, False)

    @classmethod
    def from_reference(cls, category, ref):
        return cls(category, search_ref(ref), ref)

    @staticmethod
    def play(inst):
        res = str()
        if inst.playable:
            res = f"{inst.name} playing..."
            inst.increase_play_count()
        else:
            res = f"oh no, {inst.name} seems to be broken!"
        return res

    def addinstrument:

    def getallinstruments:
    
    def addtocart:
    
    