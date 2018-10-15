#!/usr/bin/env python3

import psycopg2
import sys


def printQueryResult(titleToPrint, sql, dbConn):
    print(titleToPrint)
    print("")
    q = "COPY (%s) TO STDOUT WITH CSV HEADER DELIMITER '\t'" % sql
    with dbConn.cursor() as curs:
        curs.copy_expert(q, sys.stdout)
    print("\n")


# Connect to local db
try:
    conn = psycopg2.connect("dbname=news user=vagrant")
except psycopg2.Error as e:
    print("An error occurred while connecting to the database")
    print("Error Number: %s" % e.pgerror)
    print("Error Details: %s" % e.diag.message_detail)
    sys.exit(1)

# Print articles hit summarization
q1_sql = "SELECT title, hit_count FROM article_hits"
printQueryResult("Top Articles:", q1_sql, conn)

# Print author hit summarization
q2_sql = "SELECT author_name, hit_count FROM author_hits"
printQueryResult("Top Authors:", q2_sql, conn)

# Print the days where the error rate was at or above 1%
q3_sql = (
        "SELECT log_date, hit_fail_rate "
        "FROM daily_hit_rate_summary "
        "WHERE hit_fail_rate >= 1.0:")
printQueryResult("Days With Error Rate >= 1%", q3_sql, conn)

# Close the db
conn.close()
