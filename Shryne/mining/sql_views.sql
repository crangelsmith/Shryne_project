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



