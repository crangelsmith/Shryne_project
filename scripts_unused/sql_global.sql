
---View **all_msgs_tf** which extracts all communication details 
-- required to make the model

SELECT DISTINCT users.id AS user_id, contacts.id AS contact_id, 
contact_types.name AS relationship, channels.name AS channel, 
feed_items.send_at AS sent_at, feed_items.body AS message, 
true AS to_from FROM feed_items
JOIN channels ON feed_items.channel_id = channels.id
JOIN contacts ON feed_items.from_id = contacts.id
JOIN contact_types ON contacts.contact_type_id = contact_types.id
JOIN users ON contacts.user_id = users.id
WHERE contacts.is_fake = false
UNION 
SELECT DISTINCT users.id AS user_id, contacts.id AS contact_id, 
contact_types.name AS relationship, channels.name AS channel, 
feed_items.send_at AS sent_at, feed_items.body AS message, 
false AS to_from FROM feed_items
JOIN channels ON feed_items.channel_id = channels.id
JOIN feeds ON feeds.id = feed_items.feed_id
JOIN contacts ON contacts.id = feeds.contact_id
JOIN contact_types ON contacts.contact_type_id = contact_types.id
JOIN users ON contacts.user_id = users.id
WHERE contacts.is_fake = false AND feed_items.from_id = 0
ORDER BY 1, 2, 5;
 
-- ORDER BY at the end refers to user_id(1), contact_id(2) and sent_at(5)

-------------------------------------------------------------------------
-------------------------------------------------------------------------

--Query based on **all_msgs_tf**
-- This needs to be run to make a prediction for a single contact.

SELECT * FROM all_msgs_tf WHERE contact_id = 25364;