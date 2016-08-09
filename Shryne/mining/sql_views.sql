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


-- To get a list of the table names in alphabetical order. 
-- The names in the pdf schema are different to those actually in the database
-- I use a list comprehension in python to make it easier to read
SELECT table_name FROM information_schema.tables ORDER BY table_name

-- What input options are there to column item_type in table feed_items
SELECT DISTINCT(item_type) FROM feed_items





