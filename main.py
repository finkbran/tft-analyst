import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.environ.get("test_riot_api_key") #remember to regen this in test environment
    test_puuid = (get_puuid("MALCOLM%20SEX", "real", api_key))
    print(get_match_history(test_puuid, api_key))
    print(get_match_data("NA1_5184780757", api_key))


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

def get_ladder(api_key=None):
    root = "https://na1.api.riotgames.com/"
    chall = ("tft/league/v1/challenger?queue=RANKED_TFT")
    gm = ("tft/league/v1/grandmaster?queue=RANKED_TFT")
    master = ("tft/league/v1/master?queue=RANKED_TFT") #setup maybe we can make these vars global

    chall_response = requests.get(root + chall + "&api_key=" + api_key)
    gm_response = requests.get(root + gm + "&api_key=" + api_key)
    master_response = requests.get(root + master + "&api_key=" + api_key)

    chall_df = pd.DataFrame(chall_response.json()['entries'])
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
    print(match_data['metadata'])
    return match_data

main()

#TODO - write unencrypt function to get gameName and tagLine from summonerId
#TODO - write function to make sense of data returned from get_match_data
#TODO -read over legacy.txt, think about what functions can be readded to main
