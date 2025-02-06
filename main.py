import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.environ.get("test_riot_api_key") #remember to regen this in test environment
    get_ladder(api_key)

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
    # return id as a dictionary
    return id
def get_ladder(api_key=None):
    api_key = os.environ.get("test_riot_api_key")
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

main()

#TODO - write unencrypt function to get gameName and tagLine from summonerId

#TODO -read over legacy.txt, think about what functions can be readded to main
