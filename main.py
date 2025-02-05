import requests
def main():

    api_key = "RGAPI-497597d3-45a8-40b4-a41d-2f5b8fd1cbdd" #api key HAS TO BE GENERATED DAILY DURING DEV
    api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/MALCOLM%20SEX/real?api_key=RGAPI-a39b9d2d-83b6-49b1-b810-5653bed232c7" #request url ALSO HAS TO BE REGENERATED ALONG WITH API KEY DURING DEV
    requests.get(api_url) #send request off
    api_url + "?api_key=" + api_key  #validate request w key
    response = requests.get(api_url)
    player_info = response.json()
    print(player_info) #above requests validate key and returns id/puuid
    get_match_history()

def get_match_history(): #this function grabs the users 20 most recent games
    api_url = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/F5LZQoF46OKmJCWkco_hW1p57_jwJ6gPIH5JHjFpiU7hxpiGovjkSd-j3CbgqKPRYDvfHt7DlpmooA/ids?start=0&count=20&api_key=RGAPI-a39b9d2d-83b6-49b1-b810-5653bed232c7" #the request URL
    response = requests.get(api_url)
    match_history = response.json() #returns a list of recent games
    print(match_history)

def get_match_data():
    api_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/NA1_5202132182?api_key=RGAPI-a39b9d2d-83b6-49b1-b810-5653bed232c7'
    response = requests.get(api_url)
    match_data = response.json() #returns a dictionary in the format ['metadata', 'info']
    #NOTE 'info' is also a dictionary with keys being (['endOfGameResult', 'gameCreation', 'gameId', 'game_datetime', 'game_length', 'game_version', 'mapId', 'participants', 'queueId', 'queue_id', 'tft_game_type', 'tft_set_core_name', 'tft_set_number'])
    print(match_data['metadata'])

main()

#TODO clean up starter code (api key needs to be passed to every function that grabs data)
#TODO pull data from riot api regarding winning comps (traits, items, and augments (dont display win rate %)