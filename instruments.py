import sqlite3, requests, json, random
import instrument_model
import xml.etree.ElementTree as ET
from dataclasses import dataclass

# @dataclass
class Datastore():
    # db: str = "music_store"

    @staticmethod  
    def connectdb(db):
        global conn
        conn = sqlite3.connect(db)
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
class Review(Datastore):
    ref: int
    id: str = None
    stars: int = None
    review: str = None
    verified: bool = False
    sentiment: int = None
    db: str = "music_store.db"

    def __post_init__(self):
        pass
    
    def to_dict(self):
        return {'ref': self.ref, 'id': self.id, 'stars': self.stars, 'review': self.review, 'verified': self.verified, 'sentiment': self.sentiment}

    def verified_purchase(self):
        # self.cu = super().connectdb()
        self.cu.execute("SELECT COUNT(id) from purchase_history where ref= :ref and id= :id", {"ref": self.ref, "id": self.id})
        self.verified = bool(self.cu.fetchone()[0])
        # super().disconnectdb()
        return self.verified
        
    def post_review(self):
        self.cu = super().connectdb(self.db)
        self.cu.execute("insert into reviews VALUES (?,?,?,?,?,?)", (self.ref, self.id, self.stars, self.review, self.verified_purchase(), self.sentiment))
        self.cu.lastrowid
        if self.cu.lastrowid:
            conn.commit()
            super().disconnectdb()
            return 'Review Added'
        else:
            super().disconnectdb()
            return 'Something messed up!'

    @staticmethod
    def get_all_reviews(ref,db='music_store.db'):
        cu = Datastore.connectdb(db)
        cu.execute("SELECT * FROM reviews WHERE ref = :ref", {"ref":ref})
        reviews= [{"id":row[1], "stars":row[2], "review":row[3], "verified":row[4], "sentiment":row[5]} for row in cu.fetchall()]   
        Datastore.disconnectdb()
        return reviews


@dataclass
class Instrument(Datastore):
    ref: int = None
    name: str = None
    cat: str = None
    image: str = None
    songsterr: str = None
    reviews: list = None
    db: str = "music_store.db"

    def __post_init__(self):
        if self.ref and (self.name == None):
            self.getone()
            # review = Review(self.ref)
            # self.reviews = review.get_all_reviews()

    def getsongsterr(self):
        artists = ['Chet Atkins','Chuck Berry', 'Eric Clapton','Stevie Ray Vaughan','Jimi Hendrix']
        songster = requests.get(f'http://www.songsterr.com/a/ra/songs.xml?pattern={random.choice(artists)}')
        root = ET.fromstring(songster.content)
        songs = []
        for child in root:
            songs.append(child.attrib['id'])
        return 'http://www.songsterr.com/a/wa/song?id=' + random.choice(songs)

    def getone(self):
        cu = super().connectdb(self.db)
        cu.execute("SELECT * FROM instruments WHERE ref_num= :ref", {"ref":self.ref})
        self.ref, self.name, self.cat, self.image = cu.fetchone()
        super().disconnectdb()

    @classmethod
    def makelist(cls): # sometimes you need a tuple
        cls.cu = super().connectdb(cls.db)
        cls.cu.execute("SELECT * FROM instruments")
        return cls.cu

    @classmethod
    def getall(cls): # sometimes you need some a dict
        cls.res = [{"ref_num":row[0], "category": row[2],"name":row[1], "url":row[3]} for row in cls.makelist()]
        super().disconnectdb()
        return cls.res

    # def getreviews(self,ref):
    #     self.cu = self.connectdb()
    #     self.cu.execute("SELECT * FROM reviews WHERE ref = :ref", {"ref":ref})
    #     review = self.cu
    #     self.disconnectdb()
    #     return  self.cu
        
    def todict(self):
        if self.cat == 'string':
            self.songsterr = self.getsongsterr()
        return {"ref_num":self.ref, "category": self.cat,"name":self.name, "url":self.image, "songurl": self.songsterr, "reviews":self.reviews}

    def fromtuple(self, fields):
        self.ref, self.name, self.cat, self.image = fields

    def totuple(self):
        return (self.ref, self.name, self.cat, self.image)

    def add_instrument(self):
        try: 
            super().validate(self.ref)
        except:
            return 'Please use a 6-digit ref number'

        self.cu = super().connectdb(db)
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

