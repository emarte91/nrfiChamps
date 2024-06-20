import statsapi
import pandas as pd
import streamlit as st

def get_pitcher_stats(pitcher_name):
    """
    Retrieves and displays the pitcher's season statistics from statsapi.

    Parameters:
    pitcher_name (str): The name of the pitcher.
    """
    # Retrieve player ID for the pitcher
    player_id = next((x['id'] for x in statsapi.get('sports_players', {'season': 2024, 'gameType': 'W'})['people']
                      if x['fullName'] == pitcher_name), None)

    if player_id:
        # Retrieve pitcher's career pitching statistics
        pitcher_season_data = statsapi.player_stats(player_id, 'pitching', 'season')

        # Initialize an empty list to store data rows
        data = []

        # Split the data into lines and skip the first three lines
        lines = pitcher_season_data.strip().split('\n')[3:]
        for line in lines:
            key_value = line.split(': ')
            if len(key_value) == 2:  # Ensure it's a valid key-value pair
                key, value = key_value
                data.append([key.strip(), value.strip()])

        # Convert the data list into a pandas DataFrame
        pitcher_df = pd.DataFrame(data, columns=['Statistic', 'Value'])

        # Filter the DataFrame to include only 'wins', 'losses', and 'era'
        pitcher_stats = pitcher_df[pitcher_df['Statistic'].isin(['wins', 'losses', 'era'])]

        # Display the pitcher's name and statistics
        st.write(f"### Pitcher: {pitcher_name}")
        st.table(pitcher_stats)
    else:
        st.write(f"No player found with the name: {pitcher_name}")

def display_pitchers_stats(file_path):
    """
    Reads pitcher names from a CSV file and displays their statistics.

    Parameters:
    file_path (str): The path to the CSV file containing pitcher names.
    """
    # Read pitcher names from CSV
    pitchers_data = pd.read_csv(file_path)

    # Iterate over each pitcher and display stats
    for index, pitcher_row in pitchers_data.iterrows():
        pitcher_name = pitcher_row['pitcher_name']
        get_pitcher_stats(pitcher_name)

        # Add a divider after every two pitchers
        if (index + 1) % 2 == 0:
            st.divider()

# Path to the CSV file
file_path = 'TommorowsPitcher.csv'

# Display pitcher statistics
display_pitchers_stats(file_path)
