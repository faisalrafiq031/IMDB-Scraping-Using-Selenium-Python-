import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# Function to fetch data from SQL Server
def fetch_data_from_sql():
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Your_SQL_ServerName_Here;'  # Add your SQL server name
        'DATABASE=Your_Database_Name_Here;'  # Add your SQL database name
        'Trusted_Connection=yes;'
    )
    
    # Use pandas to read the SQL table
    query = "SELECT category, winner, nominees FROM OscarWinners_Celebs"
    df = pd.read_sql(query, connection)

    # Close the database connection
    connection.close()
    
    return df

# Function to create a bar chart for a specific category
def create_bar_chart(category_data):
    winner = category_data['winner'].values[0]
    nominees = category_data['nominees'].values[0].split(', ')  # Split nominees into a list
    
    # Select only the first three nominees
    nominees_to_display = nominees[:3]
    
    # Prepare data for plotting
    all_nominees = nominees_to_display + [winner]  # Include the winner in the nominees for display
    winner_status = ['Winner' if nom == winner else 'Nominee' for nom in all_nominees]

    # Plotting
    plt.figure(figsize=(8, 4))
    plt.barh(all_nominees, [1] * len(all_nominees), color=['gold' if status == 'Winner' else 'lightgray' for status in winner_status])
    plt.xlabel('Oscar Categories')
    plt.title(f'{category_data["category"].values[0]}')
    plt.axvline(0, color='black', linewidth=0.5)
    
    # Show the plot
    plt.show()

# Function to display categories and handle user input
def display_categories_and_plot(df):
    categories = df['category'].unique()  # Get unique categories
    category_dict = {i + 1: category for i, category in enumerate(categories)}  # Create a mapping

    while True:
        print("\nAvailable Categories:")
        for key, value in category_dict.items():
            print(f"{key}: {value}")
        print("28: See all charts in sequence")
        print("0: Exit")
        
        choice = input("Enter the number of the category you want to see (or enter '28' or '0'): ")
        
        if choice == '0':
            print("Exiting the program.")
            break
        elif choice == '28':
            for category in categories:
                create_bar_chart(df[df['category'] == category])
        else:
            try:
                category_number = int(choice)
                if category_number in category_dict:
                    category_name = category_dict[category_number]
                    create_bar_chart(df[df['category'] == category_name])
                else:
                    print("Invalid category number. Please try again.")
            except ValueError:
                print("Please enter a valid number or '0' to exit.")

# Main function to coordinate fetching and plotting
def main():
    print("Fetching data from SQL Server...")
    
    # Fetch the data
    df = fetch_data_from_sql()
    
    print(f"Fetched {len(df)} entries.")
    
    # Print the fetched data for debugging
    print(df)

    # Display categories and handle user input
    display_categories_and_plot(df)

if __name__ == "__main__":
    main() 
