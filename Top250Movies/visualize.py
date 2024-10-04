import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

# Define file paths and corresponding SQL tables Replace with yours
file_paths = {
    1: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byAlphabetic.py", "table": "IMDB_Top_250_Movies_By_alphaBetics", "name": "Alphabetic"},
    2: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byNumRate.py", "table": "IMDB_Top_250_Movies_By_numRate", "name": "Num Rating"},
    3: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byPopularity.py", "table": "IMDB_Top_250_Movies_By_popularity", "name": "Popularity"},
    4: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byRanking.py", "table": "IMDB_Top_250_Movies_By_Rank", "name": "Ranking"},
    5: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byReleaseDate.py", "table": "IMDB_Top_250_Movies_By_releaseDate", "name": "Release Date"},
    6: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byRuntime.py", "table": "IMDB_Top_250_Movies_By_Runtime", "name": "Runtime"},
    7: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\byUserRating.py", "table": "IMDB_Top_250_Movies_By_userRanking", "name": "User Rating"},
    8: {"path": r"C:\Users\Faisal\Desktop\IMDB\IMDB SCRAPING\Movies\top_250_Mv.py", "table": "IMDB_Top_250_Movies", "name": "Top 250 Movies"},
}

# Connect to SQL Server database using Windows Authentication
def connect_to_database():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Your_SQL_ServerName_Here;'  # Your sql server name
        'DATABASE=Your_Database_Name_Here;'  # Your sql database name
        'Trusted_Connection=yes;'
    )

# Load data from SQL table into DataFrame
def load_data_from_sql(table_name, conn):
    query = f"SELECT Title, IMDB_Rating FROM {table_name} ORDER BY Title"
    return pd.read_sql(query, conn)

# Function to plot a bar chart
def plot_bar_chart(df, title_suffix):
    # Get the first 6 and last 6 movies
    first_six = df.head(6)
    last_six = df.tail(6)
    movies_to_plot = pd.concat([first_six, last_six])

    # Create color gradient based on the rating
    norm = plt.Normalize(movies_to_plot['IMDB_Rating'].min(), movies_to_plot['IMDB_Rating'].max())
    cmap = mcolors.LinearSegmentedColormap.from_list("rating_cmap", ['#BDE2B9', '#4CB140']) # Gradient shade color
    
    # Generate colors based on normalized rating values
    bar_colors = cmap(norm(movies_to_plot['IMDB_Rating']))

    # Create bar chart
    plt.figure(figsize=(10, 8))
    bars = plt.barh(movies_to_plot['Title'], movies_to_plot['IMDB_Rating'], color=bar_colors)

    # Add rating values on the bars
    for bar, value in zip(bars, movies_to_plot['IMDB_Rating']):
        plt.text(value, bar.get_y() + bar.get_height()/2, f'{value:.1f}', va='center', color='black')

    plt.xlabel('IMDb Rating')
    plt.ylabel('Movie Title')
    plt.title(f'IMDb Ratings of First and Last 6 Movies from {title_suffix}')
    plt.gca().invert_yaxis()  # This will show movies in y-axis
    plt.xlim(0, 10)           # Set x-axis limit to a standard rating scale
    plt.grid(axis='x', linestyle='--', alpha=0.7)  # Add grid lines for better readability
    plt.show()

# Main function to execute the process
def main():
    # Connect to the database
    conn = connect_to_database()

    while True:
        print("Select an option to display the graph:")
        for index, value in file_paths.items():
            print(f"{index}: {value['name']}")
        print("9: View All Movies")
        print("0: Exit")

        choice = input("Enter your choice (0-9): ")
        
        if choice == '0':
            break
        elif choice == '9':
            # Loop through all file paths to plot all graphs
            for key in file_paths:
                table_name = file_paths[key]['table']
                title_suffix = file_paths[key]['name']
                try:
                    df = load_data_from_sql(table_name, conn)
                    plot_bar_chart(df, title_suffix)
                except Exception as e:
                    print(f"Error loading data from {table_name}: {e}")
        else:
            choice = int(choice)
            if choice in file_paths:
                table_name = file_paths[choice]['table']
                title_suffix = file_paths[choice]['name']
                try:
                    df = load_data_from_sql(table_name, conn)
                    plot_bar_chart(df, title_suffix)
                except Exception as e:
                    print(f"Error loading data from {table_name}: {e}")
            else:
                print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

# Execute the main function
if __name__ == "__main__":
    main()
