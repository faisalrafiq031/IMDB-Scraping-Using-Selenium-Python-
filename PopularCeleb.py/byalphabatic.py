import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import pyodbc

# Define the headers for the User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def scrape_imdb_top_celebs():
    url = 'https://www.imdb.com/chart/starmeter/?ref_=nv_cel_m&sort=alpha%2Casc'
    
    # Set up the Chrome WebDriver using WebDriver Manager
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    # Click the button to trigger the detailed view
    try:
        # Locate the button by ID and click it
        button = driver.find_element(By.ID, 'list-view-option-detailed')
        button.click()
        time.sleep(2)  # Wait for the page to load the detailed view
    except Exception as e:
        print(f"Error clicking the button: {e}")

    # Find all celebrities listed in the Starmeter table
    celebs = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

    celeb_list = []

    for celeb in celebs:
        try:
            # Extract name
            name_column = celeb.find_element(By.CLASS_NAME, 'ipc-title__text')
            name = name_column.text.strip()

            # Extract professions (Actor/Actress, Soundtrack, etc.)
            profession_elements = celeb.find_elements(By.XPATH, './/li[contains(@class, "ipc-inline-list__item sc-ada31d55-5 kwvPJV")]')

            professions = []
            for profession in profession_elements:
                professions.append(profession.text.strip())

            profession_combined = ', '.join(professions)

            # Find the ranking container
            ranking_container = celeb.find_element(By.CLASS_NAME, 'sc-b8b74125-0.ilwIpP')

            # Get the ranking number
            ranking_text = ranking_container.text.split()[0]  # Extract the first part which is the number

            # Find the span that contains the high/low rating
            ranking_info_span = ranking_container.find_element(By.CLASS_NAME, 'sc-7cc0a248-0.dzkBQg')
            ranking_info_text = ranking_info_span.text  # Extracting text for additional context

            # Determine high/low ranking based on the SVG class
            if len(ranking_container.find_elements(By.CLASS_NAME, 'ipc-icon--arrow-drop-up')) > 0:
                ranking_category = "High"
            elif len(ranking_container.find_elements(By.CLASS_NAME, 'ipc-icon--arrow-drop-down')) > 0:
                ranking_category = "Low"
            else:
                ranking_category = "Unknown"
            
            # Extract movie name from the <a> tag
            movie_link = celeb.find_element(By.CLASS_NAME, 'ipc-link--base')
            movie_name = movie_link.text.strip()
            
            # Extract Description
            description = celeb.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text.strip() if celeb.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div') else 'N/A'


            # Append the scraped data to the celeb list
            celeb_list.append({
                'Name': name,
                'Professions': profession_combined,
                'Ranking Info': ranking_text,
                'Ranking Category': ranking_category,
                'Ranking Additional Info': ranking_info_text,
                'Movie Name': movie_name,
                'Description': description,
            })

        except Exception as e:
            print(f"Error occurred while scraping a celebrity: {e}")

    driver.quit()
    return celeb_list

# Function to insert data into SQL Server
def insert_into_database(celebrities):
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
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IMDB_Popular_Celebs_Alpha_1' AND xtype='U')
    BEGIN
        CREATE TABLE IMDB_Popular_Celebs_Alpha_1  (
            id INT IDENTITY(1,1) PRIMARY KEY,  
            Name NVARCHAR(255) NOT NULL,      
            Professions NVARCHAR(MAX),         
            Ranking_Info NVARCHAR(50),         
            Ranking_Category NVARCHAR(50),      
            Ranking_Additional_Info NVARCHAR(MAX), 
            MovieName NVARCHAR(255),
            Description TEXT
        )
    END
    ''')

    # Insert data into the table
    for celeb in celebrities:
        cursor.execute(''' 
            INSERT INTO IMDB_Popular_Celebs_Alpha_1 (Name, Professions, Ranking_Info, Ranking_Category, Ranking_Additional_Info, MovieName, Description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', 
        celeb['Name'], 
        celeb['Professions'], 
        celeb['Ranking Info'], 
        celeb['Ranking Category'], 
        celeb['Ranking Additional Info'],
        celeb['Movie Name'],
        celeb['Description'],
    )
    
    connection.commit()
    cursor.close()
    connection.close()

# Main function
if __name__ == '__main__':
    # Scrape the data
    celebrities = scrape_imdb_top_celebs()
    
    if celebrities:
        print(f"Scraped {len(celebrities)} Popular Celebrities Data by Alphabetically successfully!")
        
        # Insert the scraped data into SQL Server
        insert_into_database(celebrities)
    else:
        print("No data scraped.")

