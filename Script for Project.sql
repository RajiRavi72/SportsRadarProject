use sportsradar_db;
select * from categories;
select * from competitions;
-- SQL Quries:
-- 1) 	List all competitions along with their category name
SELECT 
    c.competition_id,
    c.competition_name,
    c.parent_id,
    c.type,
    c.gender,
    cat.category_name
FROM 
    Competitions c
JOIN 
    Categories cat
ON 
    c.category_id = cat.category_id;
    
-- 2) Count the number of competitions in each category
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS competition_count
FROM 
    Categories cat
LEFT JOIN 
    Competitions c
ON 
    cat.category_id = c.category_id
GROUP BY 
    cat.category_name;
    
 -- 3) Find all competitions of type 'doubles'
 SELECT 
    competition_id,
    competition_name,
    parent_id,
    type,
    gender,
    category_id
FROM 
    Competitions
WHERE 
    type = 'doubles';
 
 -- 4)	Get competitions that belong to a specific category (e.g., ITF Men)
 SELECT 
    c.competition_id,
    c.competition_name,
    c.parent_id,
    c.type,
    c.gender,
    cat.category_name
FROM 
    Competitions c
JOIN 
    Categories cat
ON 
    c.category_id = cat.category_id
WHERE 
    cat.category_name = 'ITF Men';
    
-- 5) Identify parent competitions and their sub-competitions
SELECT 
    parent.competition_id AS parent_id,
    parent.competition_name AS parent_name,
    child.competition_id AS sub_compitition_id,
    child.competition_name AS sub_competition_name
FROM 
    Competitions parent
JOIN 
    Competitions child
ON 
    parent.competition_id = child.parent_id;
    
-- 6)	Analyze the distribution of competition types by category
SELECT 
    cat.category_name,
    c.type,
    COUNT(c.competition_id) AS competition_count
FROM 
    Categories cat
LEFT JOIN 
    Competitions c
ON 
    cat.category_id = c.category_id
GROUP BY 
    cat.category_name,
    c.type
ORDER BY 
    cat.category_name, c.type;

-- 7)	List all competitions with no parent (top-level competitions)
SELECT 
    competition_id,
    competition_name,
    type,
    gender,
    category_id
FROM 
    Competitions
WHERE 
    parent_id IS NULL;
    
    
select * from complexes;
select * from venues;

-- SQL Queries:
-- 1)	List all venues along with their associated complex name
SELECT 
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.country_code,
    v.time_zone,
    c.complex_name
FROM 
    Venues v
LEFT JOIN 
    Complexes c
ON 
    v.complex_id = c.complex_id;

-- 2)	Count the number of venues in each complex
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM 
    Complexes c
LEFT JOIN 
    Venues v
ON 
    c.complex_id = v.complex_id
GROUP BY 
    c.complex_id, c.complex_name;

-- 3)	Get details of venues in a specific country (e.g., Chile)
SELECT 
    venue_id,
    venue_name,
    city_name,
    country_name,
    country_code,
    time_zone
FROM 
    Venues
WHERE 
    country_name = 'Chile';

-- 4)	Identify all venues and their timezones
SELECT 
    venue_id,
    venue_name,
    time_zone
FROM 
    Venues;

-- 5)	Find complexes that have more than one venue
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM 
    Complexes c
JOIN 
    Venues v
ON 
    c.complex_id = v.complex_id
GROUP BY 
    c.complex_id, c.complex_name
HAVING 
    COUNT(v.venue_id) > 1;

-- 6)	List venues grouped by country
SELECT 
    country_name,
    COUNT(venue_id) AS venue_count
FROM 
    Venues
GROUP BY 
    country_name
ORDER BY 
    venue_count DESC;

-- 7)	Find all venues for a specific complex (e.g., Nacional)
SELECT 
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.country_code,
    v.time_zone
FROM 
    Venues v
JOIN 
    Complexes c
ON 
    v.complex_id = c.complex_id
WHERE 
    c.complex_name = 'Nacional';
    
select * from competitors;
select * from competitor_rankings;

 -- 1)	Get all competitors with their rank and points.
 SELECT c.name, r.ranking, r.points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id;
 
-- 2) 	Find competitors ranked in the top 5
 SELECT c.name, r.ranking
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.ranking <= 5
        ORDER BY r.ranking;
        
-- 3)	List competitors with no rank movement (stable rank)
 SELECT c.name, r.ranking, r.movement
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.movement = 0;
        
-- 4)	Get the total points of competitors from a specific country 
SELECT SUM(r.points) AS total_points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE c.country = 'Croatia';
        
-- 5)	Count the number of competitors per country
SELECT country, COUNT(*) AS count FROM Competitors GROUP BY country;

-- 6) Find competitors with the highest points in the current week
SELECT c.name, r.points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.points = (SELECT MAX(points) FROM Competitor_Rankings)

