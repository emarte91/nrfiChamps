import statsapi
from datetime import datetime, timedelta
import pytz
import streamlit as st
import pandas as pd
from unidecode import unidecode

st.set_page_config(
    page_title="NRFI Champs",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Streamlit title
st.title("Upcoming MLB Schedule")
today_date = datetime.now()
formatted_date = today_date.strftime('%m/%d')
st.sidebar.header(':blue[nrfi]Champs', divider='rainbow')
st.sidebar.success(formatted_date)

# Read pitcher data from CSV
file_path_url = 'https://raw.githubusercontent.com/emarte91/nrfiChamps/master/TomorrowsPitcherData.csv'
pitcher_data = pd.read_csv(file_path_url)

# Read MLB team batting average data from CSV
batting_data_path = 'https://raw.githubusercontent.com/emarte91/nrfiChamps/master/mlb_team_batting_averages.csv'
batting_data = pd.read_csv(batting_data_path)

pitcher_total_path = 'https://raw.githubusercontent.com/emarte91/nrfiChamps/master/PitchersTotalStatistics.csv'
pitcher_total_data = pd.read_csv(pitcher_total_path)


# Function to get team logos
def get_team_logo(team_name):
    team_logos = {
        "Arizona Diamondbacks": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Arizona_Diamondbacks_logo_teal.svg/118px-Arizona_Diamondbacks_logo_teal.svg.png",
        "Atlanta Braves": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Atlanta_Braves.svg/175px-Atlanta_Braves.svg.png",
        "Baltimore Orioles": "https://upload.wikimedia.org/wikipedia/en/thumb/7/75/Baltimore_Orioles_cap.svg/1280px-Baltimore_Orioles_cap.svg.png",
        "Boston Red Sox": "https://upload.wikimedia.org/wikipedia/en/6/6d/RedSoxPrimary_HangingSocks.svg",
        "Chicago White Sox": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Chicago_White_Sox.svg",
        "Chicago Cubs": "https://upload.wikimedia.org/wikipedia/commons/8/80/Chicago_Cubs_logo.svg",
        "Cincinnati Reds": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Cincinnati_Reds_Logo.svg/147px-Cincinnati_Reds_Logo.svg.png",
        "Cleveland Guardians": "https://img.mlbstatic.com/mlb-images/image/private/t_16x9/t_w640/mlb/uynlhw7gkkoxbiptvz9q.jpg",
        "Colorado Rockies": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c0/Colorado_Rockies_full_logo.svg/149px-Colorado_Rockies_full_logo.svg.png",
        "Detroit Tigers": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Detroit_Tigers_logo.svg/69px-Detroit_Tigers_logo.svg.png",
        "Houston Astros": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Houston-Astros-Logo.svg/100px-Houston-Astros-Logo.svg.png",
        "Kansas City Royals": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Kansas_City_Royals.svg/86px-Kansas_City_Royals.svg.png",
        "Los Angeles Angels": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Los_Angeles_Angels_of_Anaheim.svg/75px-Los_Angeles_Angels_of_Anaheim.svg.png",
        "Los Angeles Dodgers": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/LA_Dodgers.svg/502px-LA_Dodgers.svg.png",
        "Miami Marlins": "https://content.sportslogos.net/logos/54/3637/full/miami_marlins_logo_alternate_2019_sportslogosnet-7649.png",
        "Milwaukee Brewers": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/Milwaukee_Brewers_logo.svg/100px-Milwaukee_Brewers_logo.svg.png",
        "Minnesota Twins": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Minnesota_Twins_Insignia.svg/100px-Minnesota_Twins_Insignia.svg.png",
        "New York Yankees": "https://1000logos.net/wp-content/uploads/2017/05/New-York-Yankees-Logo.png",
        "New York Mets": "https://upload.wikimedia.org/wikipedia/en/7/7b/New_York_Mets.svg",
        "Oakland Athletics": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Oakland_A%27s_cap_logo.svg/120px-Oakland_A%27s_cap_logo.svg.png",
        "Philadelphia Phillies": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Philadelphia_Phillies_Insignia.svg/250px-Philadelphia_Phillies_Insignia.svg.png",
        "Pittsburgh Pirates": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Pittsburgh_Pirates_logo_2014.svg/163px-Pittsburgh_Pirates_logo_2014.svg.png",
        "San Diego Padres": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/San_Diego_Padres_%282020%29_cap_logo.svg/250px-San_Diego_Padres_%282020%29_cap_logo.svg.png?20200101200349",
        "San Francisco Giants": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/San_Francisco_Giants_Cap_Insignia.svg/224px-San_Francisco_Giants_Cap_Insignia.svg.png",
        "Seattle Mariners": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/Seattle_Mariners_logo_%28low_res%29.svg/100px-Seattle_Mariners_logo_%28low_res%29.svg.png",
        "St. Louis Cardinals": "https://upload.wikimedia.org/wikipedia/commons/3/39/St._Louis_Cardinals_insignia_logo.svg",
        "Tampa Bay Rays": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Tampa_Bay_Rays_cap_logo.svg/107px-Tampa_Bay_Rays_cap_logo.svg.png",
        "Texas Rangers": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Texas_Rangers_Insignia.svg/250px-Texas_Rangers_Insignia.svg.png",
        "Toronto Blue Jays": "https://1000logos.net/wp-content/uploads/2018/02/Toronto_Blue_Jays_Logo-640x400.png",
        "Washington Nationals": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Washington_Nationals_logo.svg/1280px-Washington_Nationals_logo.svg.png",
    }
    return team_logos.get(team_name, None)


# Get today's date
current_time = datetime.now().time()
start_time = datetime.strptime("20:00", "%H:%M").time()
end_time = datetime.strptime("23:59", "%H:%M").time()
if start_time <= current_time <= end_time:
    x = 1
else:
    x = 0
tomorrow_date = datetime.now() + timedelta(days=int(x))
formatted_date = tomorrow_date.strftime('%m/%d/%Y')

# Retrieve the schedule for tomorrow
sched = statsapi.schedule(start_date=formatted_date)

# Define the UTC timezone
utc = pytz.utc

# Define the PDT timezone
pdt = pytz.timezone('America/Los_Angeles')


# Function to get pitcher stats from the data
def get_pitcher_stats(name):
    pitcher_stats = pitcher_data[pitcher_data['Name'] == name]
    return pitcher_stats


def remove_accents(name):
    return unidecode(name)



# Iterate over each game and create individual tables

for game in sched:
    # Convert UTC datetime to PDT
    game_datetime_utc = datetime.strptime(game['game_datetime'], '%Y-%m-%dT%H:%M:%SZ')
    game_datetime_pdt = utc.localize(game_datetime_utc).astimezone(pdt)

    # Format PDT datetime string
    game_datetime_pdt_str = game_datetime_pdt.strftime('%Y-%m-%d %I:%M %p')

    away_team = game['away_name']
    away_pitcher = game['away_probable_pitcher']
    home_team = game['home_name']
    home_pitcher = game['home_probable_pitcher']

    # Get batting data for away and home teams
    away_batting_data = batting_data[batting_data['Team'] == away_team]
    home_batting_data = batting_data[batting_data['Team'] == home_team]

    # Fetch team ranks from CSV
    #away_team_rank = batting_data.loc[batting_data['Team'] == away_team, 'Rank'].iloc[0]
    #home_team_rank = batting_data.loc[batting_data['Team'] == home_team, 'Rank'].iloc[0]

    away_pitcher_total = pitcher_total_data[pitcher_total_data['PitcherName'] == away_pitcher]
    home_pitcher_total = pitcher_total_data[pitcher_total_data['PitcherName'] == home_pitcher]

    # Create a DataFrame for the current game
    game_df = pd.DataFrame({
        "Date": [game_datetime_pdt_str],
        "Away Team": [away_team],
        "Away Pitcher": [away_pitcher],
        "Home Team": [home_team],
        "Home Pitcher": [home_pitcher]
    })

    # Remove accents from pitcher names
    if away_pitcher:
        away_pitcher = remove_accents(away_pitcher)

    if home_pitcher:
        home_pitcher = remove_accents(home_pitcher)

    # Display the DataFrame for the current game
    st.write(f"### {away_team} vs {home_team}")

    away_logo = get_team_logo(away_team)
    home_logo = get_team_logo(home_team)

    # Define column layout for logos and team names
    col1, col2, col3, col4 = st.columns([1, 2, 1, 2])

    # Display home team with logo if available
    with col1:
        if away_logo:
            st.image(away_logo, width=100)

    # Display away team with logo if available
    with col2:
        if home_logo:
            st.image(home_logo, width=100)

    # Displays Game data
    st.dataframe(game_df)


    # Custom CSS for highlighting columns
    highlight_css = """
        <style>
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #ccc;
            font-size: 14px;
        }
        .custom-table th, .custom-table td {
            padding: 8px;
            text-align: center;
            border: 1px solid #ccc;
        }
        .custom-table th:nth-child(3), .custom-table td:nth-child(3) {
        background-color: #42f58d; /* Green background for 'G' column */
        }
        .custom-table th:nth-child(10), .custom-table td:nth-child(10) {
        background-color: #f59b00; /* Orange background for 'HR' column */
        }  
        .custom-table th:nth-child(9), .custom-table td:nth-child(9) {
            background-color: #ffff66; /* Yellow background for 'R' column */
        }
        .custom-table1 th:nth-child(17), .custom-table1 td:nth-child(17) {
            background-color: #f59b00; /* Orange background for 'OPS' column */
        }
        .custom-table1 th:nth-child(14), .custom-table1 td:nth-child(14) {
            background-color: #ffff66; /* Yellow background for 'AVG' column */
        }
        .custom-table1 th:nth-child(1), .custom-table1 td:nth-child(1) {
            background-color: #42f58d; /* Green background for 'Rank' column */
        </style>
        """


    def check_era_and_display(pitcher_stats, team_name):
        if 'ERA' in pitcher_stats.columns:
            era = pitcher_stats['ERA'].iloc[0]
            if era >= 4.5:
                st.write(
                    f"<p style='color:red; font-weight:bold;'>----------High risk Bet YRFI {team_name} or Over 0.5----------</p>",
                    unsafe_allow_html=True
                )
            elif era < 2.5:
                st.write(
                    f"<p style='color:green; font-weight:bold;'>----------Bet NRFI {team_name} or Under 0.5----------</p>",
                    unsafe_allow_html=True
                )
            elif 2.5 <= era <= 4.4:
                st.write(
                    "<p style='color:blue; font-weight:bold;'>----------Medium Risk Coin flip----------</p>",
                    unsafe_allow_html=True
                )

    # Display away pitcher stats
    if away_pitcher:
        away_pitcher_stats = get_pitcher_stats(away_pitcher)
        if not away_pitcher_stats.empty:
            st.write(highlight_css, unsafe_allow_html=True)
            st.text(f"#### {away_pitcher} Total Stats ####")
            st.write(away_pitcher_total.to_html(classes=["custom-table2"], index=False), unsafe_allow_html=True)
            st.write(away_pitcher_stats.to_html(classes=["custom-table"], index=False), unsafe_allow_html=True)
            if not away_batting_data.empty:
                # This is where it displays the data results
                st.text(f"#### {away_team} 1st Inning Batting Stats")
                st.write(away_batting_data.to_html(classes=["custom-table1"], index=False), unsafe_allow_html=True)



            # Check ERA and display styled message based on conditions
            if 'ERA' in away_pitcher_stats.columns:
                era = away_pitcher_stats['ERA'].iloc[0]
                if era >= 4.5:
                    st.write(
                        f"<p style='color:red; font-weight:bold;'>--------------------High Risk: Bet Over +0.5 Bottom Inning---------------------</p>",
                        unsafe_allow_html=True
                    )
                    st.divider()
                elif era < 2.5:
                    st.write(
                        f"<p style='color:green; font-weight:bold;'>--------------------Safe Bet: Under -0.5 Bottom Inning-----------------------</p>",
                        unsafe_allow_html=True
                    )
                    st.divider()
                elif 2.5 <= era <= 4.4:
                    st.write(
                        "<p style='color:blue; font-weight:bold;'>--------------------Medium Risk Coin flip-----------------------</p>",
                        unsafe_allow_html=True
                    )
                    st.divider()

    if home_pitcher:
        home_pitcher_stats = get_pitcher_stats(home_pitcher)
        if not home_pitcher_stats.empty:
            st.write(highlight_css, unsafe_allow_html=True)
            st.text(f"######## {home_pitcher} Total Stats")
            st.write(home_pitcher_total.to_html(classes=["custom-table2"], index=False), unsafe_allow_html=True)
            st.write(home_pitcher_stats.to_html(classes=["custom-table"], index=False), unsafe_allow_html=True)
            if not home_batting_data.empty:
                # This is where it displays the data results
                st.text(f"#### {home_team} 1st Inning Batting Stats")
                st.write(home_batting_data.to_html(classes=["custom-table1"], index=False), unsafe_allow_html=True)

            # Check ERA and display styled message based on conditions
            if 'ERA' in home_pitcher_stats.columns:
                era = home_pitcher_stats['ERA'].iloc[0]
                if era >= 4.5:
                    st.write(
                        f"<p style='color:red; font-weight:bold;'>--------------------High Risk: Bet Over +0.5 Top Inning--------------------</p>",
                        unsafe_allow_html=True
                    )
                elif era < 2.5:
                    st.write(
                        f"<p style='color:green; font-weight:bold;'>-------------------- Safe Bet: Under -0.5 Top Inning--------------------</p>",
                        unsafe_allow_html=True
                    )
                elif 2.5 <= era <= 4.4:
                    st.write(
                        "<p style='color:blue; font-weight:bold;'>--------------------Medium Risk Coin Flip--------------------</p>",
                        unsafe_allow_html=True
                    )

    #if not away_pitcher_stats.empty and not home_pitcher_stats.empty:
     #   if (away_pitcher_stats['ERA'].iloc[0] >= 4.5) and (
      #          home_pitcher_stats['ERA'].iloc[0] >= 4.5) and away_team_rank < 25 and home_team_rank < 25:
       #     st.write(
       #         "<p style='color:orange; font-weight:bold;'>----------Both Teams Have Terrible Pitchers: Bet YRFI 1st Inning----------</p>",
       #         unsafe_allow_html=True)
       # elif (away_pitcher_stats['ERA'].iloc[0] <= 2.5) and (
        #        home_pitcher_stats['ERA'].iloc[0] <= 2.5) and away_team_rank > 4 and home_team_rank > 4:
         #   st.write(
         #       "<p style='color:purple; font-weight:bold;'>----------Both Teams Have Great Pitchers: Bet NRFI 1st Inning----------</p>",
          #      unsafe_allow_html=True)

    # Add a divider
    st.divider()
    st.divider()
