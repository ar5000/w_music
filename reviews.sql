PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE reviews(
review_id INTEGER PRIMARY KEY AUTOINCREMENT,
t TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ref INT,
id TEXT,
stars INT,
review TEXT,
verified INT,
sentiment INT,
foreign key (ref) references instruments(ref_num)
foreign key (id) references creds(id));
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(44444,'Kyle',4,'',1,3);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Miguel',5,'I really love my new Tubano',1,5);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Kyle',1,'I really hate my new Tubano',1,0);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Kyle',2,'My new Tubano is out of tune',1,0);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Miguel',1,'I really dislike my new tubano',0,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Miguel',5,'I play my new Tubano all the time',0,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Miguel',5,'Can''t wait to get home and play my new tubano',1,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'Miguel',4,'This tubano really toots my horn',1,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'',2,'I bought this tubano from another store and really sucked',1,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(203574,'',5,'customer service was great',0,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(303685,'Kyle',4,'I love playing "Somewhere Over the Rainbow"',0,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(777777,'Kyle',5,'We need more cow bell',1,NULL);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(8888,'Kyle',5,'I love my new Vuvuzela!  I play it every day and it sounds so good.',1,2);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(8888,'Kyle',2,'It''s really noisy and out of tune',1,0);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(8888,'Kyle',1,'This one makes a bad sound',1,0);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(8888,'Kyle',1,'This one makes a bad sound.',1,-1);
INSERT INTO reviews (ref,id,stars,review,verified,sentiment) VALUES(777777,'Kyle',5,'We need more cow bell',1,0);
COMMIT;
