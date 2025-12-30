import platform
import discord
import asyncio
import colorama
from colorama import Fore, Style
from os import system
from serverclone import Clone

colorama.init(autoreset=True)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

system("cls" if platform.system() == "Windows" else "clear")

print(f"""{Fore.RED}

██╗░░██╗██╗████████╗  ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
██║░░██║██║╚══██╔══╝  ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
███████║██║░░██║░░░  ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██████╔╝
██╔══██║██║░░░██║░░░  ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██╔══██╗
██║░░██║██║░░░██║░░░  ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██║░░██║
╚═╝░░╚═╝╚═╝░░░╚═╝░░░  ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
{Style.RESET_ALL}
        {Fore.MAGENTA}Developed by: HIT{Style.RESET_ALL}
""")

token = input(f'{Fore.CYAN}Introduce tu token:\n> {Style.RESET_ALL}')
guild_source_id = input(f'{Fore.CYAN}ID del servidor que quieres clonar:\n> {Style.RESET_ALL}')
guild_target_id = input(f'{Fore.CYAN}ID del servidor donde quieres pegar:\n> {Style.RESET_ALL}')

@client.event
async def on_ready():
    print(f"{Fore.YELLOW}Conectado como: {client.user}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Clonando servidor...{Style.RESET_ALL}")

    source_guild = client.get_guild(int(guild_source_id))
    target_guild = client.get_guild(int(guild_target_id))

    if not source_guild or not target_guild:
        print(f"{Fore.RED}❌ Error: No estoy en uno de los servidores o no tengo permisos.{Style.RESET_ALL}")
        await client.close()
        return

    try:
        await Clone.guild_edit(target_guild, source_guild)
        await Clone.roles_delete(target_guild)
        await Clone.channels_delete(target_guild)
        role_map = await Clone.roles_create(target_guild, source_guild)
        category_map = await Clone.categories_create(target_guild, source_guild, role_map)
        await Clone.channels_create(target_guild, source_guild, role_map, category_map)
        await Clone.emojis_delete(target_guild)
        await Clone.emojis_create(target_guild, source_guild)
        print(f"{Fore.GREEN}✅ ¡Servidor clonado con éxito!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error durante la clonación: {e}{Style.RESET_ALL}")

    await asyncio.sleep(5)
    await client.close()

client.run(token, bot=False)
