import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.environ.get("test_riot_api_key") #remember to regen this in test environment
    test_puuid = (get_puuid("Spica", "001", api_key))
    #print(get_match_history(test_puuid, api_key))
    #print(get_match_data("NA1_5184780757", api_key))
    live_game_info(api_key)


def get_puuid(gameName=None, tagLine=None, api_key=None):
    link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    response = requests.get(link)

    return response.json()['puuid']

def get_name_tagline(puuid=None, api_key=None):
    link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?{api_key}'

    response = requests.get(link)


    id = {
        'gameName': response.json()['gameName'],
        'tagLine': response.json()['tagLine'],
    }
    # return id as a dictionary key gameName value tagLine
    return id

def get_ladder(api_key=None): #should we display this in game? or just use this for scikit analysis?
    root = "https://na1.api.riotgames.com/"
    chall = ("tft/league/v1/challenger?queue=RANKED_TFT")
    gm = ("tft/league/v1/grandmaster?queue=RANKED_TFT")
    master = ("tft/league/v1/master?queue=RANKED_TFT")

    chall_response = requests.get(root + chall + "&api_key=" + api_key)
    gm_response = requests.get(root + gm + "&api_key=" + api_key)
    master_response = requests.get(root + master + "&api_key=" + api_key)

    chall_df = pd.DataFrame(chall_response.json()['entries']) #convert api response to a dataframe for chall-master
    gm_df = pd.DataFrame(gm_response.json()['entries'])
    master_df = pd.DataFrame(master_response.json()['entries'])
    ladder = pd.concat([chall_df, gm_df, master_df]).reset_index(drop=True)
    ladder = ladder.drop(columns='rank')
    ladder = ladder.reset_index(drop=False)
    ladder = ladder.rename(columns={'index': 'rank'})
    ladder['rank'] += 1
    print(ladder) #returns players rank masters+ as a dataframe

def get_match_history(puuid=None,api_key=None, start = 0, count = 20): #this function grabs the users 20 most recent games
    api_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?{start}&{count}&api_key={api_key}" #the request URL
    response = requests.get(api_url)
    match_history = response.json() #returns an array of recent games (default is 0-20, but can be changed by user)
    print(match_history)
    return match_history
def get_match_data(match_id=None, api_key=None,): #look at regions to allow options - or should it lock to user's region?
    api_url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}'
    response = requests.get(api_url)
    match_data = response.json() #returns a dictionary in the format ['metadata', 'info']
    #NOTE 'info' is also a dictionary with keys being (['endOfGameResult', 'gameCreation', 'gameId', 'game_datetime', 'game_length', 'game_version', 'mapId', 'participants', 'queueId', 'queue_id', 'tft_game_type', 'tft_set_core_name', 'tft_set_number'])
    return match_data

def individual_match_info(match_id=None, api_key=None, puuid=None): #not functional yet, this function will grab data from an individual match, units, traits played, etc
    game = get_match_data(match_id, api_key)
    metadata = game['metadata']
    info = game['info']
    participants = metadata['participants']
    game_version = metadata['data_version']
    players = info['participants']
    #not functional yet
    player = players[participants.index(puuid)]

def live_game_info(api_key=None): #this is a demo of
    #match_id = metadata['match_id']
    #participants = metadata['participants']
   # game_version = metadata['data_version']
    #players = info['participants']
    player_info = input("Enter a player name and tagline separated by '#' (ex MALCOLM SEX#real): ")
    player_info = player_info.split('#')
    if len(player_info) < 2:
        print("Please enter the player name and tagline separated by '#'")
    else:
        player_name = player_info[0]
        tagline = player_info[1]
        puuid = get_puuid(player_name, tagline, api_key)
        print(get_match_history(puuid, api_key))
        match_num = input("Enter a match ID: ")
        game = get_match_data(match_num, api_key)
        #metadata = game['metadata']
        info = game['info']
        #match_id = metadata['match_id']
        #participants = metadata['participants']
        #game_version = metadata['data_version']
        players = info['participants']
        df_players = pd.DataFrame.from_dict(players)
        df_players = df_players.drop(columns="companion")
        units_exploded_df = df_players.explode('units')
        units_flat = pd.json_normalize(units_exploded_df["units"])
        units_exploded_df = units_exploded_df.reset_index(drop=True)
        units_flat = units_flat.reset_index(drop=True)
        df_final = pd.concat([units_exploded_df.drop(columns=['units']), units_flat], axis=1)
        players_units = df_final.groupby(["riotIdGameName", "riotIdTagline"]).agg({
            'gold_left': 'first',
            'last_round': 'first',
            'level': 'first',
            'placement': 'first',
            'character_id': lambda x: list(x),  # functions to throw the follwoing in a list
            'itemNames': lambda x: list(x),
            'rarity': lambda x: list(x),
            'tier': lambda x: list(x),
        }).reset_index()
        players_in_match = players_units
        players_in_match["RiotName"] = players_units.apply(
            lambda row: row['riotIdGameName'] + "#" + row['riotIdTagline'], axis=1)
        players_in_match.drop(columns=['riotIdGameName', 'riotIdTagline'], inplace=True)
        print(players_units["RiotName"].unique())
        specific_player = input("Enter a player name and tagline separated by '#': ")
        records = []
        for _, row in players_in_match.iterrows():
            riot_name = row['RiotName']
            for unit, items, tier in zip(row['character_id'], row['itemNames'], row['tier']):
                records.append({
                    "RiotName": riot_name,
                    "unit": unit,
                    "items": items,
                    "tier": tier
                })
        df_units = pd.DataFrame(records)
        my_units = df_units[df_units["RiotName"] == specific_player]

        for idx, row in my_units.iterrows():
            unit = row["unit"]
            tier = row["tier"]
            items = row["items"]

            #turn items list into a string
            items_str = ", ".join(items) if items else "None"
            print(f"Unit: {unit}")
            print(f"Tier: {tier}")
            print(f"Items: {items_str}")
            print("-" * 40)


main()

#TODO - write unencrypt function to get gameName and tagLine from summonerId
#TODO - write function to make sense of data returned from get_match_data
#TODO -read over legacy.txt, think about what functions can be readded to main
