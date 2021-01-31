import sqlite3, requests, json, random
import instrument_model
import xml.etree.ElementTree as ET
from dataclasses import dataclass

class Datastore():
    @staticmethod  
    def connectdb():
        global conn
        conn = sqlite3.connect("music_store.db")
        return conn.cursor()

    @staticmethod
    def disconnectdb():
        conn.close()


    def validate(self, ref):
        if len(str(ref)) < 6:
            raise ref_too_short
        if len(str(ref)) > 6:
            raise ref_too_long


@dataclass
class Instrument(Datastore):
    ref: int = None
    name: str = None
    cat: str = None
    image: str = None
    songsterr: str = None

    def __post_init__(self):
        if self.ref and (self.name == None):
            self.getone()

    def getsongsterr(self):
        artists = ['Chet Atkins','Chuck Berry', 'Eric Clapton','Stevie Ray Vaughan','Jimi Hendrix']
        songster = requests.get(f'http://www.songsterr.com/a/ra/songs.xml?pattern={random.choice(artists)}')
        root = ET.fromstring(songster.content)
        songs = []
        for child in root:
            songs.append(child.attrib['id'])
        return 'http://www.songsterr.com/a/wa/song?id=' + random.choice(songs)

    def getone(self):
        cu = super().connectdb()
        cu.execute("SELECT * FROM instruments WHERE ref_num= :ref", {"ref":self.ref})
        self.ref, self.name, self.cat, self.image = cu.fetchone()
        super().disconnectdb()

    @classmethod
    def makelist(cls): # sometimes you need a tuple
        cls.cu = super().connectdb()
        cls.cu.execute("SELECT * FROM instruments")
        return cls.cu

    @classmethod
    def getall(cls): # sometimes you need some a dict
        cls.res = [{"ref_num":row[0], "category": row[2],"name":row[1], "url":row[3]} for row in cls.makelist()]
        super().disconnectdb()
        return cls.res
        
    def todict(self):
        if self.cat == 'string':
            self.songsterr = self.getsongsterr()
        return {"ref_num":self.ref, "category": self.cat,"name":self.name, "url":self.image, "songurl": self.songsterr}

    def fromtuple(self, fields):
        self.ref, self.name, self.cat, self.image = fields

    def totuple(self):
        return (self.ref, self.name, self.cat, self.image)

    def add_instrument(self):
        try: 
            super().validate(self.ref)
        except:
            return 'Please use a 6-digit ref number'

        self.cu = super().connectdb()
        self.cu.execute("INSERT INTO instruments VALUES (?,?,?,?)", self.totuple())
        added_ref_num = self.cu.lastrowid

        if added_ref_num == self.ref:
            conn.commit()
            super().disconnectdb()
            return 'Success!'
        else:
            super().disconnectdb()
            return 'oops, something happened please ask the administrator'

    def update_instrument(self):
        self.cu = super().connectdb()

        self.cu.execute("UPDATE instruments SET name = :name, category = :cat, image = :image where ref_num = :ref", {"name":self.name, "cat":self.cat, "image":self.image, "ref":self.ref})
        rowcount = self.cu.rowcount
        if rowcount > 0:
            conn.commit()
            super().disconnectdb()
            return 'update success'
        else:
            return 'update failed'
        

class ref_too_short(ValueError):
    pass

class ref_too_long(ValueError):
    pass

    # def increase_play_count(self):
    #     self.played += 1

    # @classmethod
    # def non_playable(cls, cat, name):
    #     return cls(cat, name, False)

    # @classmethod
    # def from_reference(cls, cat, ref):
    #     return cls(cat, search_ref(ref), ref)

    # @staticmethod
    # def play(inst):
    #     res = str()
    #     if inst.playable:
    #         res = f"{inst.name} playing..."
    #         inst.increase_play_count()
    #     else:
    #         res = f"oh no, {inst.name} seems to be broken!"
    #     return res



#     def login(self, username, password):

#     def logout(self):

#     def connect(self, filename='music_store.db'):
#         self.conn = sqlite3.connect(filename)
#         self.cu = self.conn.cursor()

#     def disconnect(self):
#         self.conn.close()

#     def get_instrument(self, ref_num):
#         cursor.execute("SELECT * FROM instruments WHERE ref_num= :ref", "ref":ref_num)
#         return ???

#     def setsomedatat(self, fields):
#        cursor.execute("INSERT INTO instruments VALUES (?,?,?,?)", fields)
#        return 

