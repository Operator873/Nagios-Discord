import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

HOOK = "https://discordapp.com/api/webhooks/id/token"
KEYS = ['type', 'servdesc', 'host', 'hostaddr', 'servstate', 'date', 'output']

def codecolor(type):
    clr_red = 13632027
    clr_yel = 16098851
    clr_grn = 8311585

    if type == 'PROBLEM':
        return clr_red
    elif type == 'RECOVERY':
        return clr_grn
    else:
        return clr_yel

def main(nagIn):
    cmd = nagIn.pop(0)
    data = {KEYS[i]: nagIn[i] for i in range(len(KEYS))}
    if data['hostaddr'] == "127.0.0.1":
        data['hostaddr'] = "10.10.3.5"
    line1 = "***" + data['type'] + "*** " + data['host'] + " - " + data['servdesc'] + ": " + data['servstate']
    line2 = data['hostaddr'] + " " + data['output']

    webhook = DiscordWebhook(url=HOOK)
    # create embed object for webhook
    embed = DiscordEmbed(title=line1, description=line2, color=codecolor(data['type']))

    # add fields to embed
    embed.add_embed_field(name='Timestamp', value=data['date'])

    # add embed object to webhook
    webhook.add_embed(embed)

    res = webhook.execute()
    # print(res) ## For debugging

main(sys.argv)
