from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyodbc

# Function to scrape IMDb Oscar winners and nominees
def scrape_imdb_winners():
    url = 'https://www.imdb.com/oscars/?ref_=nv_ev_csegosc'
    
    # Set up the Chrome WebDriver using WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Open the IMDb Oscars page
    driver.get(url)

    # Wait for the winner menu option to load
    try:
        winner_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/event/ev0000003/2024/1/?ref_=fea_eds_top-1_2')]"))
        )
        winner_menu.click()
    except:
        print("Winner menu not found.")
        driver.quit()
        return []
    
    # Wait for the winner page to load
    time.sleep(3)
    
    # Try to get the main article section
    try:
        winners_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article'))
        )
    except:
        print("Winners section not found.")
        driver.quit()
        return []
    
    # Scrape data for each category
    categories = winners_section.find_elements(By.CLASS_NAME, 'event-widgets__award-category')

    # Extract the data into a list of tuples
    scraped_data = []

    for category in categories:
        # Category name
        try:
            category_name = category.find_element(By.CLASS_NAME, 'event-widgets__award-category-name').text
        except:
            category_name = "Unknown Category"

        # Winner (movie)
        try:
            winner_element = category.find_element(By.CLASS_NAME, 'event-widgets__winner-badge').find_element(By.XPATH, '..')
            winner = winner_element.find_element(By.CLASS_NAME, 'event-widgets__nominee-name').text
            
            # Get the names associated with the winner
            winner_nominees_elements = winner_element.find_elements(By.CLASS_NAME, 'event-widgets__nominee-name')
            winner_nominees = [nom.text for nom in winner_nominees_elements]
            winner_nominees_str = ', '.join(winner_nominees)
        except:
            winner = 'No winner'
            winner_nominees_str = 'No winner nominees'

        # Nominees (excluding the winner)
        nominees = category.find_elements(By.CLASS_NAME, 'event-widgets__nominee-name')
        all_nominees = [nominee.text for nominee in nominees if nominee.text != winner]
        nominees_str = ', '.join(all_nominees)

        # Append to the list (category, winner, winner nominees, other nominees)
        scraped_data.append((category_name, winner, winner_nominees_str, nominees_str))

    # Close the Selenium WebDriver
    driver.quit()

    return scraped_data


# Function to store the scraped data into SQL Server
def store_in_sql_server(data):
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Your_SQL_ServerName_Here;'  # Add your SQL server name
        'DATABASE=Your_Database_Name_Here;'  # Add your SQL database name
        'Trusted_Connection=yes;'
    )
    
    cursor = connection.cursor()

    # SQL query to create the table if it doesn't exist
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='OscarWinners_Celebs' AND xtype='U')
    CREATE TABLE OscarWinners_Celebs (
        id INT IDENTITY(1,1) PRIMARY KEY,
        category VARCHAR(255),
        winner VARCHAR(255),
        winner_nominees TEXT,
        nominees TEXT
    );
    """
    
    # Execute the table creation query
    cursor.execute(create_table_query)

    # SQL query to insert data into the table
    insert_query = """
    INSERT INTO OscarWinners_Celebs (category, winner, winner_nominees, nominees)
    VALUES (?, ?, ?, ?)
    """
    
    # Loop through the scraped data and insert into the table
    for category, winner, winner_nominees, nominees in data:
        cursor.execute(insert_query, (category, winner, winner_nominees, nominees))

    # Commit the transaction
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()


# Main function to coordinate scraping and storing
def main():
    print("Starting IMDb Oscar winners scraping...")
    
    # Scrape IMDb winners and nominees
    scraped_data = scrape_imdb_winners()
    print(f"Scraped {len(scraped_data)} entries.")
    
    # Print the scraped data for debugging
    for data in scraped_data:
        print(data)
    
    # Store scraped data in SQL Server
    print("Storing data in SQL Server...")
    store_in_sql_server(scraped_data)
    
    print("Data stored successfully.")


# Entry point for the script
if __name__ == "__main__":
    main()
