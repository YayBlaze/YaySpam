from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord import app_commands
from responses import get_response
from datetime import datetime
import time

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
SERVER_ID: Final[str] = os.getenv("GUILD_ID")
secret: Final[str] =os.getenv("SECRETS")

#intents

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

#bot setup
spam_user = 'rexydoodlesss'
spam_msg = ''
spam_delay = 0
toggle_spam = False
async def spam(start_time, interation):
    print('Function success')
    await interation.response.send_message("The spamming has commenced...")
    while toggle_spam == True:
        print('Loop Run\nstart time:',start_time,'\ncurrent time:',time.time())
        duration_secconds = time.time() - start_time
        msg = 'Minute '+str(round(duration_secconds//60))+' of waiting for '+spam_msg
        print('message:',msg,'\nwaiting secconds:',duration_secconds,'\nwaiting mins:',round(duration_secconds//60),'\n---------------------------------')
        embed = discord.Embed(title=msg)
        await spam_user.send(embed=embed)
        time.sleep(spam_delay)

# #run bot
@client.event
async def on_ready() -> None:
    await tree.sync(guild=discord.Object(id=f"{SERVER_ID}"))
    await client.change_presence(activity=discord.Activity(name="spam", type=1, ))
    print(f'{client.user} is now running')
# #handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    if username == 'yayblaze' and user_message == '!stopspam':
        print('-------------------------------\nATTEMPTING STOP\n-------------------------------')
        await message.delete()
        global toggle_spam
        toggle_spam = False
        print('stoped')
    
@tree.command(
        name="spam",
        description="Spams a user | usable by yayblaze only",
        guild=discord.Object(id=f'{SERVER_ID}')
)
async def spam_cmnd(interation, user:discord.Member, message: str, delay: int):
    if interation.user.id == 749431660168216650:
        print('Command success\nuser:',user,'\nmsg:',message,'\ndelay:',delay)
        global spam_user
        global spam_msg
        global spam_delay
        global toggle_spam
        spam_user = user
        spam_msg = message
        spam_delay = delay
        toggle_spam = True
        await spam(time.time(), interation)
    else: await interation.response.send_message("You don't have the perms to do that (L)")

# @tree.command(
#         name='stop_spam',
#         description='Stops the current spamming',
#         guild=discord.object(id=f'{SERVER_ID}')
# )
# async def stop_spam(interation):
#     if interation.user.id == 749431660168216650:
#         toggle_spam = False
#main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
