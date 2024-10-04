import pyodbc
import sys

# IMDb file paths and names Replace with Yours
file_paths = {
    1: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byAlphabetic.py", "table": "IMDB_Top_250_Movies_By_alphaBetics"},
    2: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byNumRate.py", "table": "IMDB_Top_250_Movies_By_numRate"},
    3: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byPopularity.py", "table": "IMDB_Top_250_Movies_By_popularity"},
    4: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byRanking.py", "table": "IMDB_Top_250_Movies_By_Rank"},
    5: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byReleaseDate.py", "table": "IMDB_Top_250_Movies_By_releaseDate"},
    6: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byRuntime.py", "table": "IMDB_Top_250_Movies_By_Runtime"},
    7: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byUserRating.py", "table": "IMDB_Top_250_Movies_By_userRanking"},
    8: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\top_250_Mv.py", "table": "IMDB_Top_250_Movies"}
}

# Function to choose the file and corresponding SQL table
def get_user_choice():
    print("Choose the sorting option to view IMDb data from SQL table:")
    for idx, data in file_paths.items():
        print(f"{idx}. {data['path']}")
    print(f"9. Exit")  # exit from loop

    choice = int(input("\nEnter the number corresponding to your choice: "))

    if choice == 9:
        print("Exiting...")
        sys.exit()  # this will Exit if the user chooses not to view anything

    return file_paths.get(choice)

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
    # Ask user to choose sorting method or exit
    selected_file = get_user_choice()

    if selected_file:
        # Get the corresponding table name from the selected file
        table_name = selected_file['table']
        
        # Fetch and display the data from the corresponding SQL table
        fetch_data_from_table(table_name)
