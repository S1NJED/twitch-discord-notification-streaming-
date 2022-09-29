import requests, json, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep

class Twitch:
    def __init__(self):
        self.client_id = "" # YOUR CLIENT-ID
        self.client_secret = "" # YOUR SECRET CLIENT-ID
        self.webhook_url = "" # YOUR DISCORD WEBHOOK URL
        self.online = []
        self.delay = 5
    
    # create 'streamers' file if not exists
    def create_streamers(self):
        path = os.path.exists("streamers")
        if not path:
            with open('streamer', 'w') as file:
                file.write(json.dumps([]))
    
    def create_token(self):
        path = os.path.exists("token")
        if not path:
            with open('token', 'w') as file:
                pass
    
    # open streamers file and create a list
    def get_streamers_list(self):
        self.create_streamers()
        with open('streamers', 'r') as file:
            return json.loads(file.read())
    
    # HTTP requesting a token every hour.
    def fetch_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
        'client_id': self.client_id, 
        'client_secret': self.client_secret, 
        'grant_type':'client_credentials'
        }
        res = requests.post(url, headers=headers, data=data)
        r = res.json()
        token = r['access_token']
        self.create_token()
        with open('token', 'w') as file:
            file.write(token)
    
    # get token from the file
    def get_token(self):
        self.create_token()
        with open('token', 'r') as file:
            return file.read()
    
    # HTTP requesting the pfp of the streamer
    def get_pfp(self, user):
        url = 'https://api.twitch.tv/helix/users'
        parameters = {
            'login':user
        }
        token = open('token', 'r').read()
        HEADERS = {
            'Authorization':f'Bearer {token}',
            'Client-Id': self.client_id
        }

        r = requests.get(url, headers=HEADERS, params=parameters)
        return r.json()['data'][0]['profile_image_url']

    # PERSONALIZE YOUR EMBED
    def embed(self, title, username, pp, link):
        embed = DiscordEmbed(title=f"**{username}** est en live !", description=f'[{title}]({link})', color=0x9146FF)
        embed.set_author(name=username, icon_url=self.get_pfp(username))
        embed.set_thumbnail(url=pp)
        return embed
    
    def temp_check(self, streamers):
        for streamer in self.online:
            if not streamer in streamers:
                self.online.remove(streamer)
            
    # main func.
    def main(self):
        self.create_streamers()
        with open('streamers', 'r') as file:
            streamers = json.loads(file.read())
        
        url = 'https://api.twitch.tv/helix/streams'
        
        while True:
            streamers = self.get_streamers_list()
            self.temp_check(streamers)
            
            for streamer in streamers:
                
                PARAMETERS = {
                    'user_login': streamer
                }
                try:
                    token = self.get_token()
                    HEADERS = {
                        'Authorization':f'Bearer {token}',
                        'Client-Id': self.client_id
                    }
                    r = requests.get(url, headers=HEADERS, params=PARAMETERS)
                    res = r.json()
                    
                    if res['data'] == []: # OFFLINE
                        if streamer in self.online:
                            self.online.remove(streamer)
                    
                    else: # ONLINE
                        if not streamer in self.online:
                            self.online.append(streamer)
                            
                            data = res['data'][0]
                            titre = data['title']
                            username = data['user_name']
                            # sending embed
                            try: 
                                webhook = DiscordWebhook(url=self.webhook_url, content='@everyone')
                                webhook.add_embed(self.embed(titre, username, self.get_pfp(streamer), f"https://twitch.tv/{str(streamer).lower()}"))
                                webhook.execute()
                            except:
                                pass
                except:
                    # print('TOKEN OAUTH OUTDATED')
                    self.fetch_token()
                sleep(self.delay)
            sleep(self.delay)
                
if __name__ == '__main__':
    twitch = Twitch()
    twitch.main()