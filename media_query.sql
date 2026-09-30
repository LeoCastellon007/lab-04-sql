-- media_query.sql
-- Popular posts (more than 50 likes) with the author's name, most-liked first.

SELECT
    p.post_id,
    u.username,
    u.full_name,
    p.title,
    p.likes,
    p.posted_at
FROM posts AS p
JOIN users AS u ON p.user_id = u.user_id
WHERE p.likes > 50
ORDER BY p.likes DESC;
