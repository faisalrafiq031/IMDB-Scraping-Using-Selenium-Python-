-- Top 250 Movies Start Here ---------------------------------

--1 Movies top 250
drop table IMDB_Top_250_Movies;

select * from IMDB_Top_250_Movies;

--2 Movies BY Ranking Table
drop table IMDB_Top_250_Movies_By_Rank;

select * from IMDB_Top_250_Movies_By_Rank;

--3 Movies BY IMDB Rating Table
drop table IMDB_Top_250_Movies_By_userRanking;

select * from IMDB_Top_250_Movies_By_userRanking;

--4 Movies BY Release Date Table
drop table IMDB_Top_250_Movies_By_releaseDate;

select * from IMDB_Top_250_Movies_By_releaseDate;

--5 Movies BY Number of Rating Table
drop table IMDB_Top_250_Movies_By_numRate;

select * from IMDB_Top_250_Movies_By_numRate;

--6 Movies BY alphaBetics Table
drop table IMDB_Top_250_Movies_By_alphaBetics;

select * from IMDB_Top_250_Movies_By_alphaBetics;

--7 Movies BY Popularity Table
drop table IMDB_Top_250_Movies_By_popularity;

select * from IMDB_Top_250_Movies_By_popularity;

--8 Movies BY Runtime Rate Table
drop table IMDB_Top_250_Movies_By_Runtime;

select * from IMDB_Top_250_Movies_By_Runtime;

-- Top 250 Movies End Here ---------------------------------



-- Low Rated Movies Start Here ------------------------------------

--1. Movies BY lowRate Table
drop table IMDB_Top_lowRate;

select * from IMDB_Top_lowRate;

--2. Movies BY lowRate User Rating Table
drop table IMDB_Top_lowRate_byRating;

select * from IMDB_Top_lowRate_byRating;

--3. Movies BY lowRate User Rating Table
drop table IMDB_Top_lowRate_byalphabetic;

select * from IMDB_Top_lowRate_byalphabetic;

--4 Movies BY Number of Rating Table
drop table IMDB_Top_lowRate_bynumRate;

select * from IMDB_Top_lowRate_bynumRate;

--5 Movies BY Release Date Table
drop table IMDB_Top_lowRate_byrealeaseDate;

select * from IMDB_Top_lowRate_byrealeaseDate;

--6 Movies BY Popularity Table
drop table IMDB_Top_lowRate_bypopularity;

select * from IMDB_Top_lowRate_bypopularity;

--7 Movies BY Popularity Table
drop table IMDB_Top_lowRate_byRuntime;

select * from IMDB_Top_lowRate_byRuntime;

-- Lowest Rated Movies End Here ------------------------------


-- Top Box Movies Start Here ------------------------------------

drop table IMDB_Top_BoxOffice_Movies;

select * from IMDB_Top_BoxOffice_Movies;

-- Top Box Movies End Here ------------------------------------


--  Popular Celebs Start Here ------------------------------------

--1 StarMeter Popular Celebrity Table
drop table IMDB_Popular_Celebs_starMeter;

select * from IMDB_Popular_Celebs_starMeter;



--2 Alphabetic Popular Celebrity Table
drop table IMDB_Popular_Celebs_Alpha_1;

select * from IMDB_Popular_Celebs_Alpha_1;

-- Popular Celebs End Here ------------------------------------



-- TV Shows Start Here ------------------------------------

--1 TV SHOWS TOP 250 
drop table IMDB_Top_250_Shows;

select * from IMDB_Top_250_Shows;

--2 IMDB_Top_250_Shows_byRank
drop table IMDB_Top_250_Shows_byRank;

select * from IMDB_Top_250_Shows_byRank;

-- 3 by IMDB Rating

drop table IMDB_Top_250_Shows_byRating;

select * from IMDB_Top_250_Shows_byRating;

-- 4 by Release Date

drop table IMDB_Top_250_Shows_releaseDate;

select * from IMDB_Top_250_Shows_releaseDate;

-- 5 by Alphabetic 

drop table IMDB_Top_250_Shows_alphabetic;

select * from IMDB_Top_250_Shows_alphabetic;

-- 6 by Number of Rating

drop table IMDB_Top_250_Shows_Num_Rating;

select * from IMDB_Top_250_Shows_Num_Rating;

-- 7 by Popularity 

drop table IMDB_Top_250_Shows_Popularity;

select * from IMDB_Top_250_Shows_Popularity;

-- 8 by Runtime

drop table IMDB_Top_250_Shows_runtime;

select * from IMDB_Top_250_Shows_runtime;

-- TV Shows END Here ------------------------------------


-- IMDB AWARD START HERE ------------------------

drop table OscarWinners;

select * from OscarWinners;

-----------------UPDATED AWARD TABLE --------------------------

drop table OscarWinners_Celebs;

select * from OscarWinners_Celebs;

-- Update category names for the last few categories
UPDATE OscarWinners_Celebs
SET category = CASE 
    WHEN id = 24 THEN 'Honorary Award'
    WHEN id = 25 THEN 'Jean Hersholt Humanitarian Award'
    WHEN id = 26 THEN 'Scientific and Engineering Award'
    WHEN id = 27 THEN 'Technical Achievement Award'
    ELSE category
END
WHERE id IN (24, 25, 26, 27);