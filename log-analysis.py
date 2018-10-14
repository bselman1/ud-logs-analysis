import psycopg2
import sys

# Connect to local db
conn = psycopg2.connect("dbname=news user=vagrant")

#Print articles hit summarization
print("Top Articles:\n")
with conn.cursor() as curs:
	q1_sql = "SELECT title, hit_count FROM article_hits"
	q1 = "COPY (%s) TO STDOUT WITH CSV HEADER DELIMITER '\t'"%(q1_sql)
	curs.copy_expert(q1, sys.stdout)
print("\n")

#Print author hit summarization
print("Top Authors:\n")
with conn.cursor() as curs:
	q2_sql = "SELECT author_name, hit_count FROM author_hits"
	q2 = "COPY (%s) TO STDOUT WITH CSV HEADER DELIMITER '\t'"%(q2_sql)
	curs.copy_expert(q2, sys.stdout)
print("\n")

#Print the days where the error rate was at or above 1%
print("Days With Error Rate >= 1%\n")
with conn.cursor() as curs:
	q3_sql = "SELECT log_date, hit_fail_rate FROM daily_hit_rate_summary WHERE hit_fail_rate >= 1.0"
	q3 = "COPY (%s) TO STDOUT WITH CSV HEADER DELIMITER '\t'"%(q3_sql)
	curs.copy_expert(q3, sys.stdout)
print("\n")

	
#Close the db
conn.close()