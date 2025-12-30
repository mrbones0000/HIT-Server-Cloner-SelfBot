import discord	
import aiohttp
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

def print_add(msg): print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")
def print_del(msg): print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")
def print_err(msg): print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")

class Clone:

    @staticmethod
    async def roles_delete(guild):
        for role in guild.roles:
            if role.name == "@everyone":
                continue
            try:
                await role.delete()
                print_del(f"Deleted Role: {role.name}")
                await asyncio.sleep(0.7)
            except:
                print_err(f"Error Deleting Role: {role.name}")

    @staticmethod
    async def roles_create(guild_to, guild_from):
        roles = [r for r in guild_from.roles if r.name != "@everyone"]
        roles.sort(key=lambda r: r.position)
        role_map = {}

        for r in roles:
            try:
                new_role = await guild_to.create_role(
                    name=r.name,
                    permissions=r.permissions,
                    colour=r.colour,
                    hoist=r.hoist,
                    mentionable=r.mentionable
                )
                role_map[r.id] = new_role
                print_add(f"Created Role: {r.name}")
                await asyncio.sleep(1.2)
            except:
                print_err(f"Error Creating Role: {r.name}")

        roles_sorted_desc = sorted(roles, key=lambda r: r.position, reverse=True)
        for r in roles_sorted_desc:
            try:
                new_role = role_map[r.id]
                await new_role.edit(position=r.position)
                await asyncio.sleep(1.5)
            except:
                print_err(f"Error Setting Role Position: {r.name}")

        return role_map

    @staticmethod
    async def channels_delete(guild):
        for ch in guild.channels:
            try:
                await ch.delete()
                print_del(f"Deleted Channel: {ch.name}")
                await asyncio.sleep(0.7)
            except:
                print_err(f"Error Deleting Channel: {ch.name}")

    @staticmethod
    async def categories_create(guild_to, guild_from, role_map):
        cat_map = {}
        categories = sorted(guild_from.categories, key=lambda c: c.position)

        for c in categories:
            try:
                overwrites = {}
                for target, perms in c.overwrites.items():
                    if isinstance(target, discord.Role):
                        if target.id in role_map:
                            overwrites[role_map[target.id]] = perms
                        elif target.name == "@everyone":
                            overwrites[guild_to.default_role] = perms

                new_cat = await guild_to.create_category(c.name, overwrites=overwrites)
                await new_cat.edit(position=c.position)
                cat_map[c.id] = new_cat
                print_add(f"Created Category: {c.name}")
                await asyncio.sleep(1.2)
            except:
                print_err(f"Error Creating Category: {c.name}")

        return cat_map

    @staticmethod
    async def channels_create(guild_to, guild_from, role_map, cat_map):
        channels = sorted(guild_from.channels, key=lambda c: c.position)

        for ch in channels:
            try:
                category = cat_map.get(ch.category.id) if ch.category else None
                overwrites = {}

                for target, perms in ch.overwrites.items():
                    if isinstance(target, discord.Role):
                        if target.id in role_map:
                            overwrites[role_map[target.id]] = perms
                        elif target.name == "@everyone":
                            overwrites[guild_to.default_role] = perms

                if isinstance(ch, discord.TextChannel):
                    await guild_to.create_text_channel(
                        name=ch.name,
                        overwrites=overwrites,
                        topic=ch.topic,
                        category=category,
                        nsfw=ch.nsfw,
                        slowmode_delay=getattr(ch, 'slowmode_delay', 0)
                    )
                elif isinstance(ch, discord.VoiceChannel):
                    await guild_to.create_voice_channel(
                        name=ch.name,
                        overwrites=overwrites,
                        category=category,
                        user_limit=ch.user_limit,
                        bitrate=ch.bitrate
                    )
                print_add(f"Created Channel: {ch.name}")
                await asyncio.sleep(1.0)
            except:
                print_err(f"Error Creating Channel: {ch.name}")

    @staticmethod
    async def emojis_delete(guild):
        for emoji in guild.emojis:
            try:
                await emoji.delete()
                print_del(f"Deleted Emoji: {emoji.name}")
                await asyncio.sleep(0.7)
            except:
                print_err(f"Error Deleting Emoji: {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to, guild_from):
        async with aiohttp.ClientSession() as session:
            for emoji in guild_from.emojis:
                try:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            emoji_bytes = await resp.read()
                            await guild_to.create_custom_emoji(
                                name=emoji.name,
                                image=emoji_bytes
                            )
                            print_add(f"Created Emoji: {emoji.name}")
                            await asyncio.sleep(1.2)
                        else:
                            print_err(f"Error downloading emoji: {emoji.name}")
                except:
                    print_err(f"Error Creating Emoji: {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to, guild_from):
        try:
            await guild_to.edit(name=guild_from.name)
            if guild_from.icon:
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(str(guild_from.icon_url_as(format="png"))) as resp:
                            if resp.status == 200:
                                icon_bytes = await resp.read()
                                await guild_to.edit(icon=icon_bytes)
                                print_add(f"Guild Icon Changed: {guild_to.name}")
                                await asyncio.sleep(1.2)
                            else:
                                print_err("Error downloading guild icon")
                    except:
                        print_err("Error fetching guild icon")
        except:
            print_err(f"Error Editing Guild: {guild_to.name}")
