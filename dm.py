import requests as req
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import configparser
import json
import sys
import yaml
import time


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0"
sleep = 5
token_file = "token.json"

class Channel:
    def __init__(self, name, id, isAllowed=True):
        self.name = name
        self.id = id
        self.isAllowed = isAllowed

def parseChannelFile():
    channels = []
    stream = open("channels.yml", "rb")
    dictionary = dict(yaml.load(stream, Loader=yaml.FullLoader))
    for d1 in dictionary['channels']:
        channels.append(Channel(name=d1["name"], id=d1["id"], isAllowed=d1["everyoneIsAllowed"]))
    return channels

def getOAuthToken(login_auth):
    header = {'Content-Type':'application/json', 'User-agent': user_agent}
    resp = req.post("https://discord.com/api/v9/auth/login", headers=header,data=json.dumps(login_auth))
    if resp.status_code != 200:
        print("An error has occurred while attempting to authenticate. See the error message below:")
        try:
            print(json.dumps(json.loads(resp.content)["errors"], indent=3))
        except KeyError:
            print(json.dumps(json.loads(resp.content), indent=3))
        sys.exit()
        
    else:
        f = open("token.json", "w")
        f.write(json.dumps(json.loads(resp.content)))
        f.close()
        access_token = json.loads(resp.content)["token"] 
        print("Successfully Authenticated!")
        return access_token

def verifyOAuthToken():
    try:
        auth_file = json.load(open(token_file))
    except IOError:
        print("%s doesn't exist! Getting new OAuth token file." % token_file)
        return

    token = auth_file["token"]
    print("Verifying current token is still valid...")
    header = {'Content-Type':'application/json', 'Authorization': token,'User-agent': user_agent}
    resp = req.get("https://discord.com/api/v9/users/@me/library", headers=header)
    if resp.status_code != 200:
        print("OAuth token no longer valid. Getting new OAuth token.")
        return 
    print("Token is still valid!")
    return token



def postMessageToChannel(token,channel_list, message):
    header = {'Content-Type':'application/json', 'Authorization': token,'User-agent': user_agent}
    
    print("Posting message to channels now....")
    message = message +" "+ twitch_channel
    for channel in channel_list:
        print("Waiting for %s seconds..." % str(sleep))
        time.sleep(sleep)

        content_message = message
        if channel.isAllowed == False:
            content_message = removeEveryoneTag(message)
            
        c = {'content': content_message}
        resp = req.post("https://discord.com/api/v9/channels/"+ channel.id + "/messages", headers=header, data=json.dumps(c))
        if resp.status_code != 200:
            print("An error occurred when attempting to post a message to channel  %s:" % channel.name)
            print(json.dumps(json.loads(resp.content), indent=3))
        else:
            print("Message successfully posted to channel: %s!" % channel.name)


def removeEveryoneTag(message):
    return str(message).replace("@everyone", "").strip()


if __name__ == '__main__':
    parser = ArgumentParser(
    description="Python script to post a single message to multple Discord channels.",
    formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("-m", required=True, help="The message to post. Example: \"Mook becomes a space cadet! Outer Wilds VR #VR\"", dest="message")
    args = parser.parse_args()
    configParser = configparser.ConfigParser()
    configParser.read("dm.conf")
    

    discord_username = configParser.get("discord", "username").strip('"')
    discord_password = configParser.get("discord", "password").strip('"')
    
    twitch_channel = configParser.get("twitch", "twitch_channel_url").strip('"')


    login_auth = dict(login=discord_username,
                    password=discord_password,
                    undelete=False,
                    captcha_key=None,
                    login_source=None,
                    gift_code_sku_id=None)   
  
    message = args.message
    channels = parseChannelFile()
    token = verifyOAuthToken()
    if token == None:
        token = getOAuthToken(login_auth)
    postMessageToChannel(token,channels, message)