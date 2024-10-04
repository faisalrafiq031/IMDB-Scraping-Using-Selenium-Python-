import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import pyodbc
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def scrape_imdb_top_250():
    url = 'https://www.imdb.com/chart/top/?sort=release_date%2Cdesc'
    
    # Set up the Chrome WebDriver using WebDriver Manager
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    
    # Click the button to trigger the detailed view
    try:
        # Locate the button by ID and click it
        button = driver.find_element(By.ID, 'list-view-option-detailed')
        button.click()
        time.sleep(2)  # Wait for the page to load the detailed view
    except Exception as e:
        print(f"Error clicking the button: {e}")
    
    

    # Find all movies listed in the Top 250 table
    movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__c')


    movie_list = []
    

    for movie in movies:
        # Extract title
        title_column = movie.find_element(By.CLASS_NAME, 'ipc-title__text')
        full_title = title_column.text.strip()

        # Check if the title contains a period before splitting
        if '.' in full_title:
            title = full_title.split('.', 1)[1].strip()
        else:
            title = full_title  # If no period, use the entire title
        
        # Extract year
        year = movie.find_element(By.XPATH, './/span[contains(@class, "sc-b189961a-8")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-b189961a-8")]') else None
        year = int(year) if year else None

        # Extract IMDb rating
        imdb_rating = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--rating').text.strip()
        imdb_rating = float(imdb_rating) if imdb_rating else None
        
        # Extract Time (checks for hours "h" or minutes "min" in the text)
        MovieTime = movie.find_element(By.XPATH, './/span[contains(@class, "sc-b189961a-8") and (contains(text(), "h") or contains(text(), "m"))]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-b189961a-8") and (contains(text(), "h") or contains(text(), "m"))]') else 'N/A'
        
        # Genre (Movies ratings like PG, G, etc.)
        runtimeGen = movie.find_element(By.XPATH, './/span[contains(@class, "sc-b189961a-8") and (text()="Approved" or text()="Passed" or text()="PG" or text()="G" or text()="R" or text()="PG-13" or text()="NC-17" or text()="Not Rated")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-b189961a-8") and (text()="Approved" or text()="Passed" or text()="PG" or text()="G" or text()="R" or text()="PG-13" or text()="NC-17" or text()="Not Rated")]') else 'N/A'
        
        # Extract rating count
        rating_count = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-rating-star--voteCount') else 'N/A'

        # Extract description
        description = movie.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div') else 'N/A'

        # Extract director
        director = movie.find_element(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-director-item"]').text.strip() if movie.find_element(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-director-item"]') else 'N/A'

        # Extract starring 
        stars = [star.text.strip() for star in movie.find_elements(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-cast-item"]')]

        # Extract image URL
        image_element = movie.find_element(By.XPATH, './/div/img[@class="ipc-image"]')
        image_url = image_element.get_attribute('src')  # Extract the 'src' attribute from the image tag
        

        # Append the scraped data to the movie list
        movie_list.append({
            'Title': title,
            'Year': year,
            'Time': MovieTime,
            'Runtime': runtimeGen,
            'IMDb Rating': imdb_rating,
            'Rating Count': rating_count,
            'Description': description,
            'Director': director,
            'Stars': ", ".join(stars),
            'Image URL': image_url,  # Add the image URL here
            # 'Video URL': trailer_url  # Add the video URL here
        })

    driver.quit()

    return movie_list


# # Function to insert data into SQL Server
def insert_into_database(movies):
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Your_SQL_ServerName_Here;'  # Add your SQL server name
        'DATABASE=Your_Database_Name_Here;'  # Add your SQL database name
        'Trusted_Connection=yes;'
    )
    
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(''' 
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IMDB_Top_250_Movies_By_releaseDate' AND xtype='U')
    BEGIN
        CREATE TABLE IMDB_Top_250_Movies_By_releaseDate (
            id INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing primary key
            Title NVARCHAR(255) NOT NULL,      -- Title of the movie
            Year INT,                           -- Year of release
            MovieTime NVARCHAR(10),             -- Time
            Runtime NVARCHAR(10),               -- Runtime (R, PG, NC-17 etc)
            IMDB_Rating FLOAT,                  -- IMDb rating
            Rating_Count NVARCHAR(20),          -- Rating count (e.g., "2.9M")
            Description TEXT,          -- Description of the movie
            Director VARCHAR(255),             -- Director of the movie
            Stars VARCHAR(255),                -- Comma-separated list of stars
            ImageURL NVARCHAR(255),              -- URL of the movie image
            -- VideoURL NVARCHAR(255)              -- URL of the movie video trailer
        )
    END
    ''')

    # Insert data into the table
    for movie in movies:
        cursor.execute('''
            INSERT INTO IMDB_Top_250_Movies_By_releaseDate (Title, Year, MovieTime, Runtime, IMDB_Rating, Rating_Count, Description, Director, Stars, ImageURL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        movie['Title'], 
        movie['Year'], 
        movie['Time'],
        movie['Runtime'],  
        movie['IMDb Rating'], 
        movie['Rating Count'], 
        movie['Description'], 
        movie['Director'], 
        movie['Stars'], 
        movie['Image URL']  # Add the image URL to the insertion
        # movie['Video URL']   # Add the video URL here
    )
    connection.commit()
    cursor.close()
    connection.close()

# Main function
if __name__ == '__main__':
    # Scrape the data
    movies = scrape_imdb_top_250()
    
    if movies:
        print(f"Scraped {len(movies)}  movies By Release Date successfully! ")
        
        # Insert the scraped data into SQL Server
        insert_into_database(movies)
    else:
        print("No data scraped.")
