## View Creation
```
CREATE VIEW article_hits AS
(
	WITH article_with_path AS
	(
	SELECT 
	  title,
	  authors.name as author_name,
	  '/article/' || slug as article_path
	FROM articles
	INNER JOIN authors ON articles.author = authors.id
	), 
	log_ok_entry as
	(
		SELECT path
		FROM log
		WHERE status = '200 OK'
	)
	SELECT
	  article_with_path.title,
	  article_with_path.author_name,
	  COUNT(*) as hit_count
	FROM article_with_path
	INNER JOIN log_ok_entry ON log_ok_entry.path = article_with_path.article_path
	GROUP BY article_with_path.title, article_with_path.author_name
	ORDER BY hit_count DESC
);
```
```
CREATE VIEW author_hits as 
(
SELECT
  author_name,
  SUM(hit_count) as hit_count
FROM article_hits
GROUP BY author_name
ORDER BY SUM(hit_count) DESC
);
```