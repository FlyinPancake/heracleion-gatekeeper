from see import get_names_from_image
import discord
from discord.utils import get
from dotenv import dotenv_values
import os

config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def can_sender_manage_roles(message):
    return message.author.permissions_in(message.channel).manage_roles

def can_be(aa, bb):
    if aa == None:
        return False
    
    return aa.lower().endswith(bb.lower())

async def find_member(members, name):
    for mb in members:
        if can_be(mb.name, name) or can_be(mb.nick, name):
            return mb

    return None

async def assign_war_roles_from_image(message, fname, role_name):
    role = get(message.guild.roles, name=role_name)
    names = get_names_from_image(fname)
    print(f"{len(names)} names found in roster")
    membs = await message.guild.fetch_members().flatten()
    gotten = 0

    for name in names:
        member = await find_member(membs, name)
        if member != None:
            print(f"Found {name}, adding role.")
            gotten += 1
            await member.add_roles(role)

    return gotten

async def save_image_from_message_get_name(message):
    for attachment in message.attachments:
        image_types = ["png", "jpeg", "gif", "jpg"]
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            print('Got warlist attachments')
            _, ext = os.path.splitext(attachment.filename)
            final_fname = 'temp/temp'+ext
            await attachment.save(final_fname)
            return final_fname

def get_role_name_from_cmd(message):
    tokens = message.content.split(' ')
    if len(tokens) < 1:
        raise Exception('Not enough arguments')

    return tokens[1].strip()

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
        if not can_sender_manage_roles(message):
            return
        
        if message.content.startswith('!war_roles'):
            fname = await save_image_from_message_get_name(message)
            role = get_role_name_from_cmd(message)
            assigned_no = await assign_war_roles_from_image(message, fname, role)
            await message.reply(f"Added role **{role}** to **{assigned_no}** members.")

    except Exception as err:
        print('Error:')
        print(err)
        await message.reply("An error ocured and I couldn't update the war roles.")

client.run(config['DC_TOKEN'])