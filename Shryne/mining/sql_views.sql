-- Some SQL queries to get us started


-- Creating a view means you can use the name of the view as a table (but it 
-- doesn't store it as a table, it just reruns the query every time you call it)
-- e.g. This view gives you all the messages for a user (i.e, any of us can put 
-- in our own names)
CREATE VIEW viewname AS
SELECT body FROM feed_items
JOIN contacts ON contacts.id = feed_items.from_id 
JOIN users ON users.id = contacts.user_id
WHERE users.first_name = 'string' AND users.last_name = 
'string' LIMIT 1


-- This view gives us a list of users which have both real and fake accounts
CREATE VIEW real_fake_users AS
SELECT DISTINCT fakes.userid from fakes, reals
WHERE fakes.userid = reals.userid


-- This tells us how many users have fake and real accounts (might be a bug)
-- and uses. This returns a count of 4724.

SELECT count(*) FROM real_fake_users

-- This give us the names of users that have both real and fake 
SELECT users.first_name, users.last_name from users
JOIN contacts ON
users.id = contacts.user_id
JOIN real_fake_users
ON real_fake_users.userid = contacts.id

-- to get no_of_messages_by_total for Alex
SELECT analytics_metrics.no_of_message_responses_by_total FROM analytics_metrics
JOIN analytics_scores ON analytics_scores.id = 
analytics_metrics.analytics_score_id
JOIN contacts ON contacts.id = analytics_scores.contact_id
JOIN users ON users.id = contacts.user_id
WHERE users.first_name = 'Alexander'
AND users.last_name = 'Green';

-- To get a list of the table names in alphabetical order. 
-- The names in the pdf schema are different to those actually in the database
-- I use a list comprehension in python to make it easier to read
SELECT table_name FROM information_schema.tables ORDER BY table_name

-- What input options are there to column item_type in table feed_items
SELECT DISTINCT(item_type) FROM feed_items


-- Find the names of columns in a table
SELECT column_name,data_type 
FROM information_schema.columns 
WHERE table_name = 'table_name';

-- created a view named reals, which contains all of the user.ids, contacts.ids
-- for all users and their contacts, where is_fake = false
-- likewise for a view named fake

-- fakes
SELECT users.id AS userid, contacts.id AS contactid, contacts.is_fake
FROM users JOIN contacts ON users.id = contacts.user_id
WHERE contacts.is_fake = true;

-- reals
SELECT users.id AS userid, contacts.id AS contactid, contacts.is_fake
FROM users JOIN contacts ON users.id = contacts.user_id
WHERE contacts.is_fake = false;

-- in theory, there should be no users with contacts who are both real and fake
-- however, by running the following we found that there are 4724 who have both
-- fake and real friends

SELECT COUNT(DISTINCT fakes.userid)
FROM fakes
JOIN reals
ON fakes.userid = reals.userid
GROUP BY fakes.is_fake;

-- in addition, the vast majority of the fake accounts have the following names

Anne Fuller
Connor Hayes
Danielle Park
Bethany Lewis
Garrett Jones
Ethan Lau
Cody Stewart

-- finally, those contacts who have names different from those above, but are still fake are]

SELECT DISTINCT userid, first_name, last_name
FROM fakes_names
WHERE first_name
NOT IN ('Connor', 'Danielle', 'Garrett','Anne','Ethan','Bethany','Cody');


 userid |  first_name   |      last_name
--------+---------------+---------------------
  12081 | Jeremy        | Mandell
  11994 | Anneb         | Fuller
   6459 | Jancos Archiv | Jancovic
   4867 | Piggy         | Huang
   6065 | Carlos        | Sutter
  11985 | Danielle edit | Park edit
   7078 | Paulo         | Capelo
   7098 | Molly         | Derichs
   7717 | Sawsan        | Seikaly
   8119 | Pieter        | Hayes
   8050 | @@@@@@@@@@@   | &&&&&&&&&&&&&&&&&&&
   6139 | Connorhj      | Hayes
   7264 | Schatz        | I love you
   6458 | Me & Houma    | Love
   6190 |       מישהו    |     פעם
   7872 | Moor          | Hayes
   9100 | Anna          | K.
   7471 | Aldeize       | Serra de santa

-- getting analytics scores

SELECT sent_by_user, sent_by_contact, sent_total
FROM analytics_metrics
JOIN analytics_scores
ON analytics_metrics.analytics_score_id = analytics_scores.id
JOIN contacts
ON analytics_scores.contact_id = contacts.id
JOIN users
ON contacts.user_id = users.id
WHERE users.first_name = 'Alexander'
AND users.last_name = 'Green';

-- As we're still unsure about the exact nature of the analytics scores, we'd
-- add our own way of calculating them via this view
-- It creates one row per message in the database
-- Schema is
-- user_id | contact_id | relationship | channel | sent_at | message_id
-- Should be able to use this to make initial histograms
-- Can call this is SELECT * FROM all_messages_metadata


CREATE VIEW all_messages_metadata AS SELECT DISTINCT users.id AS user_id,
contacts.id AS contact_id, contact_types.name AS relationship, channels.name
AS channel, feed_items.send_at AS sent_at feed_items.id AS message_id
FROM feed_items
JOIN channels
ON feed_items.channel_id = channels.id
JOIN contacts
ON feed_items.from_id = contacts.id
JOIN contact_types
ON contacts.contact_type_id = contact_types.id
JOIN users
ON contacts.user_id = users.id
WHERE contacts.is_fake = false;


-- Same as above, but with the actual message instead of the message_id
-- user_id | contact_id | relationship | channel | sent_at | message
CREATE VIEW all_messages AS SELECT DISTINCT users.id AS user_id,
contacts.id AS contact_id, contact_types.name AS relationship, channels.name
AS channel, feed_items.send_at AS sent_at, feed_items.body AS message
FROM feed_items
JOIN channels
ON feed_items.channel_id = channels.id
JOIN contacts
ON feed_items.from_id = contacts.id
JOIN contact_types
ON contacts.contact_type_id = contact_types.id
JOIN users
ON contacts.user_id = users.id
WHERE contacts.is_fake = false;