from discord import client
from utils import save_image_from_message_get_name
from client import client
from discord.utils import get
from see_bio import process_bio_image

TARGET_ROLE = "Verified Syndicate"
GUILD_ID = 901802275306106910

async def verify_member(message):
    guild = client.get_guild(GUILD_ID)
    role = get(guild.roles, name=TARGET_ROLE)

async def handle_verification(message):
    if message.content.startswith('!verify_me'):
        fname = await save_image_from_message_get_name(message)
        res = process_bio_image(fname)
        await message.reply(f"You are verified now!")