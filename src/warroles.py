from discord.utils import get
from seewarlist import get_names_from_image
from utils import save_image_from_message_get_name

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

def get_role_name_from_cmd(message):
    tokens = message.content.split(' ')
    if len(tokens) < 1:
        raise Exception('Not enough arguments')

    return tokens[1].strip()

async def handle_war_roles_message(message):
    if not can_sender_manage_roles(message):
        return
        
    if message.content.startswith('!war_roles'):
        fname = await save_image_from_message_get_name(message)
        role = get_role_name_from_cmd(message)
        assigned_no = await assign_war_roles_from_image(message, fname, role)
        await message.reply(f"Added role **{role}** to **{assigned_no}** members.")