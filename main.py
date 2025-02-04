import requests
def main():

    api_key = "RGAPI-72ab4a38-81d2-490b-9280-752115dcff86" #api key HAS TO BE GENERATED DAILY
    api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/MALCOLM%20SEX/real?api_key=RGAPI-72ab4a38-81d2-490b-9280-752115dcff86" #request url
    requests.get(api_url) #send request off
    api_url + "?api_key=" + api_key  #validate request w key
    response = requests.get(api_url)
    player_info = response.json()
    print(player_info)

main()

#TODO read through overwolf api for round by round analysis to be provided post game (riot provides end of match stats)
#TODO pull data from riot api regarding winning comps (traits, items, and augments (dont display win rate %)