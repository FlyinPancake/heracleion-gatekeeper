from discord import client
from utils import save_image_from_message_get_name
from client import client
from discord.utils import get
from see_bio import process_bio_image
from config import config

TARGET_ROLE = "Verified Syndicate"
GUILD_ID = int(config['GUILD_ID'])

def can_be(aa, bb):
    if aa == None:
        return False
    
    return aa.lower().endswith(bb.lower())

async def find_member(members, name):
    for mb in members:
        if can_be(mb.name, name) or can_be(mb.nick, name):
            return mb

    return None

async def try_add_guild_role(guild, company, member):
    try:
        rname = f"Company:{company.lower().replace(' ', '-')}"
        role = get(guild.roles, name=rname)
        await member.add_roles(role)
        return True
    except:
        return False

def does_sender_already_have_role(message, role):
    mem = message.author
    for mm in role.members:
        if mm.id == mem.id:
            return True

    return False

async def verify_member(message, fname):
    guild = client.get_guild(GUILD_ID)
    role = get(guild.roles, name=TARGET_ROLE)
    has = does_sender_already_have_role(message, role)
    if has:
        await message.reply(f"Already verified!")
        return

    res = process_bio_image(fname)
    print(res)
    if not res["matches"]:
        await message.reply(f"Verification request denied!")
        return

    membs = await guild.fetch_members().flatten()
    member = await find_member(membs, res['name'])

    if member == None or member.id != message.author.id:
        await message.reply(f"Verification request denied!")
        return

    await member.add_roles(role)
    await try_add_guild_role(guild, res['company'], member)

    await message.reply(f"You **{res['name']}** from **{res['company']}** are verified now!")

async def handle_verification(message):
    if message.content.startswith('!verify_me'):
        fname = await save_image_from_message_get_name(message)
        await verify_member(message, fname)