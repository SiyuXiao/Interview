# Insert Puzzle

The DELETE and UPDATE expressions are expensive in a columnar database that is constantly
changing and contains millions of records. Rewrite the following table
schema to evict a record using only the INSERT expression and write the SELECT
query that allows you to query the database without dealing with the duplicated records.

```sql
CREATE TABLE table (
  advertiser_id   BIGINT,
  advertiser_name VARCHAR(250),
  campaign_id     BIGINT,
  campaign_name   VARCHAR(250),
  creative_id     BIGINT,
  creative_name   VARCHAR(250),
  impressions     BIGINT,
  clicks          BIGINT,
  conversions     BIGINT
)
PRIMARY KEY (advertiser_id, campaign_id, creative_id)
;
```

The following query will sum up the duplicates. Fix the query after modifying the schema to remove the duplicates while querying.
```sql
SELECT advertiser_name, campaign_name, creative_name, SUM(impressions), SUM(clicks), SUM(conversions)
FROM table
GROUP BY 1,2,3
ORDER BY 4,5,6 ASC
;
```

The `PRIMARY KEY` keyword is not a SQL standard PRIMARY KEY. This sentence
only points out the sort key, so the (advertiser_id, campaign_id,
creative_id) key can be repeated along the table but in the SELECT query
those records should not be shown more than one at a time.

You can add as many columns as you want to that schema, but you must NOT remove any of the present columns.
You can add more queries to insert and select the records if you wish.

* How do I know if a record is being duplicated?
- The following query will print the duplicated records `SELECT advertiser_id, campaign_id, creative_id, count(*) AS cnt FROM table GROUP BY 1,2,3 HAVING cnt > 1`

A example of the expected input/output:
```sql
INSERT INTO table VALUES (1, 'Advertiser 1', 1, 'Campaign 1', 1, 'Creative 1', 20, 10, 1, ...more columns);
INSERT INTO table VALUES (1, 'Advertiser 1', 1, 'Campaign 1', 1, 'Creative 1', 30, 10, 4, ...more columns);
INSERT INTO table VALUES (1, 'Advertiser 1', 1, 'Campaign 1', 1, 'Creative 1', 87, 35, 8, ...more columns);

INSERT INTO table VALUES (2, 'Advertiser 2', 2, 'Campaign 2', 2, 'Creative 2', 42, 11, 6, ...more columns);
INSERT INTO table VALUES (2, 'Advertiser 2', 2, 'Campaign 2', 2, 'Creative 2', 58, 14, 6, ...more columns);
INSERT INTO table VALUES (2, 'Advertiser 2', 2, 'Campaign 2', 2, 'Creative 2', 98, 30, 8, ...more columns);

SELECT
  advertiser_name,
  campaign_name,
  creative_name,
  SUM(impressions),
  SUM(clicks),
  SUM(conversions)
FROM ... the table or view you are going to use
... any join or where sentence here to filter out the records
GROUP BY 1,2,3
ORDER BY 4,5,6
 advertiser_name | campaign_name | creative_name | sum | sum | sum 
-----------------+---------------+---------------+-----+-----+-----
 Advertiser 1    | Campaign 1    | Creative 1    |  87 |  35 |   13
 Advertiser 2    | Campaign 2    | Creative 2    |  98 |  30 |   8
```

You can try to solve this problem in a PostgreSQL database but should work in any other SQL-like database.
