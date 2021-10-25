import discord
from config import config
from warroles import handle_war_roles_message

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
