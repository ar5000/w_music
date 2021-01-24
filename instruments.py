import sqlite3, requests, json, random
import instrument_model
import xml.etree.ElementTree as ET


class Instrument:



    playable = True
    def __init__(self, ref= None, name=None, cat=None, image=None):
        self.ref = ref
        self.name = name
        self.cat = cat
        self.image = image
        self.songsterr = None
        if self.ref and (self.name == None):
            self.getone()
        # self.playable = playable
        # self.played = 0
        

    def __str__(self):
        return f"This is a {self.name} and is a {self.cat} instrument"

    def __repr__(self):
        return f"Instrument({self.ref}, {self.name}, {self.cat})"

    @classmethod
    def connectdb(cls):
        global conn
        conn = sqlite3.connect("music_store.db")
        return conn.cursor()

    @classmethod
    def disconnectdb(cls):
        conn.close()

    def getsongsterr(self):
        artists = ['Chet Atkins','Chuck Berry', 'Eric Clapton','Stevie Ray Vaughan','Jimi Hendrix']
        songster = requests.get(f'http://www.songsterr.com/a/ra/songs.xml?pattern={random.choice(artists)}')
        root = ET.fromstring(songster.content)
        songs = []
        for child in root:
            songs.append(child.attrib['id'])
        return 'http://www.songsterr.com/a/wa/song?id=' + random.choice(songs)

    def getone(self):
        cu = self.connectdb()
        cu.execute("SELECT * FROM instruments WHERE ref_num= :ref", {"ref":self.ref})
        self.ref, self.name, self.cat, self.image = cu.fetchone()
        self.disconnectdb()

    @classmethod
    def makelist(cls):
        cls.cu = cls.connectdb()
        cls.cu.execute("SELECT * FROM instruments")
        return cls.cu

    @classmethod
    def getall(cls):
        cls.res = [{"ref_num":row[0], "category": row[2],"name":row[1], "url":row[3]} for row in cls.makelist()]
        cls.disconnectdb()
        return cls.res
        
    def todict(self):
        if self.cat == 'string':
            self.songsterr = self.getsongsterr()
        return {"ref_num":self.ref, "category": self.cat,"name":self.name, "url":self.image, "songurl": self.songsterr}

    def fromtuple(self, fields):
        self.ref, self.name, self.cat, self.image = fields

    def totuple(self):
        return (self.ref, self.name, self.cat, self.image)




    def addinstrument(self):
        pass

    def getallinstruments(self):
        pass
    def addtocart(self):
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





# class Datastore:
#     def __init__(self):

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
