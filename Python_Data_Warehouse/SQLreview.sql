SELECT id, last_name, city, LENGTH(city) AS LENGTH
FROM employees
ORDER BY length, last_name;

--------------------------

SELECT SUBSTRING('This is the first', 9, 10) as substring_extraction;

//POSITION()
//SUBSTRING()
--------------------------

SELECT *
FROM artist AS art
INNER JOIN album as alb
ON art.artist_id = alb.artis_id

--------------------------

SELECT * FROM artist as alb
INNER JOIN album AS alb
USING(artist_id)

---------------------------
 

SELECT * FROM artist as art
LEFT JOIN album as alb
ON art.artis_id = alb.artis_id

--------------------------

SELECT * FROM album
WHERE artis_id IN (SELECT artis_id FROM artist);

