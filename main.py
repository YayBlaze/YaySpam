from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord import app_commands
from datetime import datetime
import time

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
SERVER_ID: Final[str] = os.getenv("GUILD_ID")

#intents

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

#bot setup
class Spam:
    def __init__(self):
        self.user = None
        self.msg = None
        self.delay = 1
        self.toggle = None
        self.start = None
        self.interaction = None
        self.waiting_time = None
        self.count = 0
        self.type = None
        self.countToggle = None
    def toggle_spam(self):
        self.toggle = not self.toggle
    def set_user(self, user):
        self.user = user
    def set_msg(self, msg):
        self.msg = msg
    def set_delay(self, delay):
        self.delay = delay
    def set_toggle(self, state):
        self.toggle = state
    def set_start(self, start_time):
        self.start = start_time
    def set_int(self, interaction):
        self.int = interaction
    def set_waiting_time_toggle(self, state):
        self.waiting_time = state
    def increment_count(self):
        self.count+=1
    def set_type(self, type):
        self.type = type
    def set_count_toggle(self, state):
        self.countToggle = state
Victims = [Spam() for i in range(10)]

# OLD
# async def spam(interation):
#     print('Function sucess \nVictims:', ", ".join([i.user.display_name for i in Victims if i.user != None]))
#     await interation.response.send_message("The spamming has commenced...")
#     toggles = []
#     for i in Victims:
#         toggles.append(i.toggle)
#     while True in toggles:
#         for i in Victims:
#             if i.msg != None:
#                 print('Loop Run\nstart time:',i.start,'\ncurrent time:',time.time())
#                 duration_secconds = time.time() - i.start
#                 msg = 'Minute '+str(round(duration_secconds//60))+' of waiting for '+i.msg
#                 print('message:',msg,'\nwaiting secconds:',duration_secconds,'\nwaiting mins:',round(duration_secconds//60),'\n---------------------------------')
#                 embed = discord.Embed(title=msg)
#                 await i.user.send(embed=embed)
#         time.sleep(Victims[0].delay)

async def spam(interation):
    print('Function sucess \nVictims:', ", ".join([i.user.display_name for i in Victims if i.user != None]))
    await interation.response.send_message("The spamming has commenced...")
    await loop(interation)
    
async def loop(interation):
    for i in Victims:
        if i.toggle:
            print('Loop run for ', i.user,'\nStart time: ',i.start,'\nCurrent Time',time.time())
            if i.waiting_time:
                duration_secconds = time.time() - i.start
                msg = 'Minute '+str(round(duration_secconds//60))+' of waiting for '+i.msg
                print('message:',msg,'\nwaiting secconds:',duration_secconds,'\nwaiting mins:',round(duration_secconds//60),'count: ',i.count,'\n---------------------------------')
            elif i.countToggle:
                msg = f"{i.msg} #{i.count}"
                print('meassage: ', msg, '\ncount: ', i.count)
            else: 
                msg = i.msg
                print('meassage: ', msg, '\ncount: ', i.count)
            embed = discord.Embed(title=msg)
            i.increment_count()
            if i.type == 0: await i.user.send(embed=embed)
            elif i.type == 1: await interation.channel.send(content=f"<@{i.user.id}>", embed=embed)
            
    time.sleep(Victims[0].delay)
    await loop(interation)

#run bot
@client.event
async def on_ready() -> None:
    await tree.sync(guild=discord.Object(id=f"{SERVER_ID}"))
    await client.change_presence(activity=discord.Activity(name="spam", type=1, ))
    print(f'{client.user} is now running')
#handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    username: str = str(message.author)
    user_message: str = message.content
    if username == 'yayblaze' and user_message == '!stopspam':
        print('-------------------------------\nATTEMPTING STOP\n-------------------------------')
        await message.delete()
        for i in Victims:
            i.toggle = False
        await message.channel.send(content="Stopped All Spamming")
        print('-------------------------------\nSTOPED\n-------------------------------')

@tree.command(
        name="spam",
        description="Spams a user | usable by yayblaze only",
        guild=discord.Object(id=f'{SERVER_ID}')
)
async def spam_cmnd(interation, user:discord.Member, message: str, delay: int, wait: bool, count: bool, type: int):
    if interation.user.id == 749431660168216650:
        print('Spam Command success\nuser:',user,'\nmsg:',message,'\ndelay:',delay)
        for i in Victims:
            if not i.toggle:
                i.set_user(user)
                i.set_msg(message)
                i.set_delay(delay)
                i.set_toggle(True)
                i.set_start(time.time())
                if wait and count: await interation.response.send_message(content="You cannot turn on wait and count", ephermial=True)
                i.set_waiting_time_toggle(wait)
                i.set_count_toggle(count)
                if type < 0 or type > 1: await interation.response.send_message(content="Invalid Type!", ephemeral=True)
                i.set_type(type)
                break
        await spam(interation)
    else: await interation.response.send_message(content="You don't have the perms to do that (L)", ephemeral=True)

@tree.command(
        name="info",
        description="Gives info on the bot",
        guild=discord.Object(id=f'{SERVER_ID}')
)
async def info(interation):
    print("Info Command Run")
    embed = discord.Embed(title="YaySpam", description="This is a discord bot I made for spamming my friends", colour=discord.Colour.yellow())
    embed.add_field(name="Command",value="The /spam command, used to start the bot, can only be run by YayBlaze. If you really want to use it ask me.", inline=False)
    await interation.response.send_message(embed=embed)
    
    
@tree.command(
        name='stop_spam',
        description='Stops the given spamming | usable by yayblaze only',
        guild=discord.Object(id=f'{SERVER_ID}')
)
async def stop_spam(interation, index: int):
    if interation.user.id == 749431660168216650:
        i = Victims[index]
        if i.toggle:
            i.toggle_spam()
            await interation.response.send_message(content=f"Stopped Spamming {i.user.display_name}.")
        else: await interation.response.send_message(content='This is not a valid index', ephemeral=True)
    else: await interation.response.send_message(content="You don't have the perms to do that (L)", ephemeral=True)

 
#main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
