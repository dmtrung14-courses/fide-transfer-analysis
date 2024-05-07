import numpy as np
import pandas as pd
import requests
import concurrent.futures

data = pd.read_csv('data_rated.csv')
data = data.iloc[:, 1:]
data = data.dropna()
data = data.reset_index(drop=True)

# for each id in the column ID, fetch data from https://fide-api.vercel.app/player_info/?fide_id={id}&history=false
# and append the data to the dataframe

data['World Rank'] = np.nan
data['National Rank'] = np.nan
data['Name'] = np.nan
data['Title'] = np.nan
data['Rating'] = np.nan


def fetch_data(id):
    url = f"https://fide-api.vercel.app/player_info/?fide_id={id}&history=true"
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        
        world_rank_all = player_data['world_rank_all']
        national_rank_all = player_data['national_rank_all']
        world_rank_active = player_data['world_rank_active']
        national_rank_active = player_data['national_rank_active']
        name = player_data['name']
        title = player_data['fide_title']
        rating = player_data["history"][0]["classical_rating"]

        data.loc[data['ID'] == id, 'World Rank'] = world_rank_active if world_rank_active != 0 else world_rank_all
        data.loc[data['ID'] == id, 'National Rank'] = national_rank_active if national_rank_active != 0 else national_rank_all
        data.loc[data['ID'] == id, 'Name'] = name
        data.loc[data['ID'] == id, 'Title'] = title
        data.loc[data['ID'] == id, 'Rating'] = rating
        print("Finished fetching data for: ", player_data["name"])

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(fetch_data, data['ID'])

data = data.dropna(subset=['Name'])

data.drop_duplicates(subset='ID', inplace=True)

data.to_csv('data_rated.csv', index=False)
