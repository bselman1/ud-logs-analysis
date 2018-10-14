## Overview
Python based script to analyze the database logs of an online news service serving articles. The results of the script are printed to stdout as tab delimited tables and answer the following:
* Top articles titles by hit count.
* Top authors by hit count.
* Days where the error rate was >= 1.0%

## Views
Three summary views were created as follows:

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
```
CREATE VIEW daily_hit_rate_summary AS
(
  WITH t1 AS
  (
    SELECT
      date(time) as log_date,
      SUM(CASE WHEN status = '200 OK' THEN 1 ELSE 0 END) as hit_success,
      SUM(CASE WHEN status = '404 NOT FOUND' THEN 1 ELSE 0 END) as hit_fail,
      COUNT(*) as hit_total
    FROM log
    GROUP BY date(time)
  )
  SELECT
    t1.log_date,
    t1.hit_total,
    t1.hit_success,
    t1.hit_fail,
    (t1.hit_success::decimal / t1.hit_total) * 100 as hit_success_rate,
    (t1.hit_fail::decimal / t1.hit_total)::numeric * 100 as hit_fail_rate
  FROM t1
);
```

## Execution
Print to the console:
```
python3 log-analysis.py
```

Print to a file:
```
python3 log-analysis.py > output.txt
```