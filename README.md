# StreamingTools

This repo contains helper scripts to automate some of the more tedious tasks of streaming.

## dm.py 

### Description
Send a single message to multiple Discord channels

### Requriements
```
Python3

The following Python modules:
requests
argparse
configparser
pyyaml
```

### Install

Clone the repo:
`git clone https://github.com/CaptMook/StreamingTools.git`

Install the required Python modules:
`python3 -m pip install -r requirements.txt`

Create the required `dm.conf` file:

- Linux: `cp dm.conf.sample dm.conf`
- Windows: `copy dm.conf.sample dm.conf`

Create the required `channels.conf` file: 
- Linux: `cp channels.conf.sample channels.conf`
- Windows: `copy channels.conf.sample channels.conf`

Update the `dm.conf` file with your Discord credentials and Twitch channel URL:

```
[discord]
username = jdoe@gmail.com
password = jdoe123

[twitch]
twitch_channel_url = https://twitch.tv/jdoe
```

Update `channels.yml` with channel names with their channel ID. Below is the contents of `channels.yml.sample`:

**Note:** If the `everyoneIsAllowed` parameter is set to `False` for a channel, then the script will remove the `@everyone` tag from the posted message, if it exists, for that channel.

```
channels:
  - name: "Channel Name"
    id: "ChannelID"
    everyoneIsAllowed: False

  - name: "Channel Name"
    id: "Channel ID"
    everyoneIsAllowed: True
```

**How To Find The Channel ID**

1. Log in to Discord via the Web App, https://discord.com (e.g. NOT the Desktop App)
2. Navigate to the channel you want to post in
3. Copy the CHANNELID value from your browser bar. Example: https://discord.com/channels/12345678910123/CHANNELID


### Usage

Usage:
```bash
usage: dm.py [-h] -m MESSAGE

Python script to post a single message to multple Discord channels.

optional arguments:
  -h, --help  show this help message and exit
  -m MESSAGE  The message to post. Example: "Mook becomes a space cadet! Outer Wilds VR #VR"
```

Success Example:
```bash
python3 dm.py -m Mook becomes a space cadet! Outer Wilds VR #VR
Successfully Authenticated!
Posting message to channels now....
Message successfully posted to channel: Mooks Channel - General!
Message successfully posted to channel: Mooks Channel - clips and highlights!
```

Result:

![](success.png)