import discord
from client import client
from config import config
from warroles import handle_war_roles_message
from verification import handle_verification
import sys
from see_bio import process_bio_image

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        await handle_war_roles_message(message)
        await handle_verification(message)

    except Exception as err:
        print('Error:')
        print(err)
        await message.reply("An error ocured and I couldn't do what you asked me to do.")

client.run(config['DC_TOKEN'])