import requests, json, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep

client_id = "" # YOUR CLIENT-ID
client_secret = "" # YOUR SECRET CLIENT-ID
webhook_url = "" # YOUR DISCORD WEBHOOK URL
online = []
delay = 5

# create 'streamers' file if not exists
def create_streamers():
    path = os.path.exists("streamers")
    if not path:
        with open('streamer', 'w') as file:
            file.write(json.dumps([]))

def create_token():
    path = os.path.exists("token")
    if not path:
        with open('token', 'w') as file:
            pass

# open streamers file and create a list
def get_streamers_list():
    create_streamers()
    with open('streamers', 'r') as file:
        return json.loads(file.read())

# HTTP requesting a token every hour.
def fetch_token():
    url = 'https://id.twitch.tv/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
    'client_id': client_id, 
    'client_secret': client_secret, 
    'grant_type':'client_credentials'
    }
    res = requests.post(url, headers=headers, data=data)
    r = res.json()
    token = r['access_token']
    create_token()
    with open('token', 'w') as file:
        file.write(token)

# get token from the file
def get_token():
    create_token()
    with open('token', 'r') as file:
        return file.read()

# HTTP requesting the pfp of the streamer
def get_pfp(user):
    url = 'https://api.twitch.tv/helix/users'
    parameters = {
        'login':user
    }
    token = open('token', 'r').read()
    HEADERS = {
        'Authorization':f'Bearer {token}',
        'Client-Id': client_id
    }

    r = requests.get(url, headers=HEADERS, params=parameters)
    return r.json()['data'][0]['profile_image_url']

# PERSONALIZE YOUR EMBED
def embed(title, username, pp, link):
    embed = DiscordEmbed(title=f"**{username}** est en live !", description=f'[{title}]({link})', color=0x9146FF)
    embed.set_author(name=username, icon_url=get_pfp(username))
    embed.set_thumbnail(url=pp)
    return embed

def temp_check(streamers):
    for streamer in online:
        if not streamer in streamers:
            online.remove(streamer)
    
# main func.
def main():
    create_streamers()
    with open('streamers', 'r') as file:
        streamers = json.loads(file.read())

    url = 'https://api.twitch.tv/helix/streams'

    while True:
        streamers = get_streamers_list()
        temp_check(streamers)
        
        for streamer in streamers:
            
            PARAMETERS = {
                'user_login': streamer
            }
            try:
                token = get_token()
                HEADERS = {
                    'Authorization':f'Bearer {token}',
                    'Client-Id': client_id
                }
                r = requests.get(url, headers=HEADERS, params=PARAMETERS)
                res = r.json()
                
                if res['data'] == []: # OFFLINE
                    if streamer in online:
                        online.remove(streamer)
                
                else: # ONLINE
                    if not streamer in online:
                        online.append(streamer)
                        
                        data = res['data'][0]
                        titre = data['title']
                        username = data['user_name']
                        # sending embed
                        try: 
                            webhook = DiscordWebhook(url=webhook_url, content='@everyone')
                            webhook.add_embed(embed(titre, username, get_pfp(streamer), f"https://twitch.tv/{str(streamer).lower()}"))
                            webhook.execute()
                        except:
                            pass
            except:
                # print('TOKEN OAUTH OUTDATED')
                fetch_token()
            sleep(delay)
        sleep(delay)
                
if __name__ == '__main__':
    main()