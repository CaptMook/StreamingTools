import requests as req
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import configparser
import json
import sys

class Channel:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
def getOAuthToken(login_auth):
    header = {'Content-Type':'application/json'}
    resp = req.post("https://discord.com/api/v9/auth/login", headers=header,data=json.dumps(login_auth))
    if resp.status_code != 200:
        print("An error has occurred while attempting to authenticate. See the error message below:")
        try:
            print(json.dumps(json.loads(resp.content)["errors"], indent=3))
        except KeyError:
            print(json.dumps(json.loads(resp.content), indent=3))
        sys.exit()
        
    else:
        access_token = json.loads(resp.content)["token"]
        print("Successfully Authenticated!")
        return access_token


def postMessageToChannel(token,channel_list, message):
    header = {'Content-Type':'application/json', 'Authorization': token}
    message = message +" "+ twitch_channel
    c = {'content': message}
    print("Posting message to channels now....")
    for channel in channel_list:
        resp = req.post("https://discord.com/api/v9/channels/"+ channel.id + "/messages", headers=header, data=json.dumps(c))
        if resp.status_code != 200:
            print("An error occurred when attempting to post a message to channel  %s:" % channel.name)
            print(json.dumps(json.loads(resp.content), indent=3))
        else:
            print("Message successfully posted to channel: %s!" % channel.name)



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
  
   
# "CHANNEL NAME" can be any value you want.
# "CHANNEL ID" must be a valid channel ID value. Refer to the beginning of this file on how to obtain the correct channel ID.

    channels = []
    f = open("channels.conf","r").readlines()
    for line in f:
        cname = line.split(":")[0]
        cid = line.split(":")[1].strip("\n")
        channels.append(Channel(cname,cid))

    message = args.message

    token = getOAuthToken(login_auth)
    postMessageToChannel(token,channels, message)