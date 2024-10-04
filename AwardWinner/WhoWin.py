import pyodbc

# Function to connect to SQL Server and fetch data for a specific category
def fetch_category_data(category):
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Your_SQL_ServerName_Here;'  # Add your SQL server name
        'DATABASE=Your_Database_Name_Here;'  # Add your SQL database name
        'Trusted_Connection=yes;'
    )
    
    cursor = connection.cursor()
    
    # SQL query to select data for the specified category
    query = "SELECT winner FROM OscarWinners_Celebs WHERE category = ?"
    
    cursor.execute(query, (category,))
    
    # Fetch all winners for the specified category
    winners = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return [winner[0] for winner in winners]  # Extract winner names from tuples

# Main function to interact with the user
def main():
    # List of categories to display to the user
    categories = {
        1: "Best Motion Picture of the Year",
        2: "Best Performance by an Actor in a Leading Role",
        3: "Best Performance by an Actress in a Leading Role",
        4: "Best Performance by an Actor in a Supporting Role",
        5: "Best Performance by an Actress in a Supporting Role",
        6: "Best Achievement in Directing",
        7: "Best Original Screenplay",
        8: "Best Adapted Screenplay",
        9: "Best Achievement in Cinematography",
        10: "Best Achievement in Film Editing",
        11: "Best Achievement in Production Design",
        12: "Best Achievement in Costume Design",
        13: "Best Sound",
        14: "Best Achievement in Makeup and Hairstyling",
        15: "Best Achievement in Music Written for Motion Pictures (Original Score)",
        16: "Best Achievement in Music Written for Motion Pictures (Original Song)",
        17: "Best Achievement in Visual Effects",
        18: "Best Documentary Feature",
        19: "Best Animated Feature Film",
        20: "Best Animated Short Film",
        21: "Best Live Action Short Film",
        22: "Best Documentary Short Film",
        23: "Best International Feature Film",
        24: "Honorary Award",
        25: "Jean Hersholt Humanitarian Award",
        26: "Scientific and Engineering Award",
        27: "Technical Achievement Award"
    }

    print("Available Categories:")
    for key, value in categories.items():
        print(f"{key}: {value}")

    while True:
        # Ask the user to choose a category or exit
        choice = input("Enter the number of the category you want to see (or enter '0' to exit): ")
        
        if choice == '0':
            break
        
        try:
            category_number = int(choice)
            if category_number in categories:
                category_name = categories[category_number]
                winners = fetch_category_data(category_name)
                
                if winners:
                    # Print winner in the desired format
                    print(f"Winner for '{category_name}' is: {', '.join(winners)}")
                else:
                    print(f"No winners found for '{category_name}'.")
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Please enter a valid number or '0' to exit.")

if __name__ == "__main__":
    main()
