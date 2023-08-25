#!/usr/bin/python3

import sys
import urllib.parse

from discord_webhook import DiscordEmbed, DiscordWebhook

HOOK = "https://discordapp.com/api/webhooks/id/token"  # UPDATE WITH YOUR WEBHOOK
KEYS = ["type", "servdesc", "host", "hostaddr", "servstate", "time", "output"]
DOMAIN = "your.website.com"  # UPDATE WITH YOUR URL/DOMAIN


def codecolor(alerttype):
    clr_red = 13632027
    clr_yel = 16098851
    clr_grn = 8311585

    if alerttype == "PROBLEM":
        return clr_red
    elif alerttype == "RECOVERY":
        return clr_grn
    else:
        return clr_yel


def main(nag_in):
    _cmd = nag_in.pop(0)
    data = {KEYS[i]: nag_in[i] for i in range(len(KEYS))}
    host = urllib.parse(data["host"])
    serv = urllib.parse(data["servdesc"])

    link = (
        f"https://{DOMAIN}/nagios/cgi-bin/extinfo.cgi?type=2&host={host}&service={serv}"
    )

    line1 = (
        f"**<{data['type']}>** {data['host']} - {data['servdesc']}: {data['servstate']}"
    )
    line2 = f"{data['hostaddr']} {data['output']}"

    webhook = DiscordWebhook(url=HOOK)
    # create embed object for webhook
    embed = DiscordEmbed(title=line1, description=line2, color=codecolor(data["type"]))
    embed.set_author(name="Open Nagios service detail", url=link)

    # set timestamp
    embed.set_timestamp(int(data["time"]))

    # add embed object to webhook
    webhook.add_embed(embed)

    webhook.execute()


if __name__ == "__main__":
    main(sys.argv)
