# Transact puzzle

The RedShift data warehouse uses the COPY command to insert rows from
a tab-separated data file into a table.  For example:
```
  COPY meta.placemap FROM 's3://my-data/placemap.tsv';
```

Neither the COPY nor the TRUNCATE commands can be used inside a
RedShift transaction; and RedShift doesn't support UPDATE commands.

Write SQL code to replace the contents of table meta.placemap such
that the update appears instantaneous to other queries.  More
specifically, other meta.placemap queries must never see duplicate
rows or an empty meta.placemap table.

Answer:

When I firstly read this question, I have an opinion: 

Can I create a outer table?  When I need to transact, I can get the data from the outer table. 

So I target the opinion to search on the Internet and get the following SQL code:



CREATE EXTERNAL TABLE external_schema.table_name  

(
  col1 data_type
  ,col2 data_type
  ...
 )
 ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION  's3://my-data/placemap.tsv' 
;

CREATE TABLE schema.table_name 
(
  col1 data_type
  ,col2 data_type
  ...
);

insert into schema.table_name
  (
    col1 
    ,col2 
    ...
  )
select 
  col1
  ,col2
from external_schema.table_name  

where ...-- filter Duplicate data 
;
commit;

-- result: schema.table 