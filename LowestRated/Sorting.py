import pyodbc        # To get data from sql server 
import os            # Importing os to handle file paths
import sys           # This is used to exit the program

# IMDb file paths and names
file_paths = {
    1: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byAlphabetic.py", "table": "IMDB_Top_lowRate_byalphabetic"},
    2: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byNumRating.py", "table": "IMDB_Top_lowRate_bynumRate"},
    3: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byPopularity.py", "table": "IMDB_Top_lowRate_bypopularity"},
    4: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byReleaseDate.py", "table": "IMDB_Top_lowRate_byrealeaseDate"},
    5: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byRuntime.py", "table": "IMDB_Top_lowRate_byRuntime"},
    6: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\byUserRating.py", "table": "IMDB_Top_lowRate_byRating"},
    7: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\LowestRated\lowestRated.py", "table": "IMDB_Top_lowRate"}
}

# Function to choose the file and corresponding SQL table
def get_user_choice():
    print("Choose the sorting option to view IMDb data from SQL table:")
    for idx, data in file_paths.items():
        # Extract the filename using os.path.basename
        file_name = os.path.basename(data['path'])
        print(f"{idx}. {file_name}")
    print(f"0. Exit")  # Option to exit

    choice = int(input("\nEnter the number corresponding to your choice: "))
    return choice

# Function to connect to SQL Server and fetch data from the selected table
def fetch_data_from_table(table_name):
    try:
        # SQL Server connection setup with Windows Authentication
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=Your_SQL_ServerName_Here;'  # Add your SQL server name
            'DATABASE=Your_Database_Name_Here;'  # Add your SQL database name
            'Trusted_Connection=yes;'
        )

        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch all rows from the table
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print(f"No data found in table {table_name}.")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error fetching data from SQL table: {e}")

# Main function
if __name__ == '__main__':
    while True:  # Loop until the user chooses to exit
        choice = get_user_choice()

        if choice == 0:
            print("Successfully Exit the program...")
            sys.exit()  # Exit the program
        elif choice in file_paths:
            selected_file = file_paths[choice]
            table_name = selected_file['table']
            fetch_data_from_table(table_name)  # Fetch and display the data
        else:
            print("Invalid choice, please try again.")
