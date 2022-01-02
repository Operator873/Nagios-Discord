#!/usr/bin/python3

import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

HOOK = "https://discordapp.com/api/webhooks/id/token"
KEYS = ['type', 'servdesc', 'host', 'hostaddr', 'servstate', 'time', 'output']
DOMAIN = "your.website.com"


def codecolor(alerttype):
    clr_red = 13632027
    clr_yel = 16098851
    clr_grn = 8311585

    if alerttype == 'PROBLEM':
        return clr_red
    elif alerttype == 'RECOVERY':
        return clr_grn
    else:
        return clr_yel


def main(nag_in):
    cmd = nag_in.pop(0)
    data = {KEYS[i]: nag_in[i] for i in range(len(KEYS))}

    link = "https://" + DOMAIN + "/nagios/cgi-bin/extinfo.cgi?type=2&host=" + data['host'] + "&service=" + data['servdesc']

    line1 = "**<" + data['type'] + ">** " + data['host'] + " - " + data['servdesc'] + ": " + data['servstate']
    line2 = data['hostaddr'] + " " + data['output']

    webhook = DiscordWebhook(url=HOOK)
    # create embed object for webhook
    embed = DiscordEmbed(title=line1, description=line2, color=codecolor(data['type']))
    embed.set_author(name='Open Nagios service detail', url=link)

    # set timestamp
    embed.set_timestamp(int(data['time']))

    # add embed object to webhook
    webhook.add_embed(embed)

    res = webhook.execute()


main(sys.argv)
