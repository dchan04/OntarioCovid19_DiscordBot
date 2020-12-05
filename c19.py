import os
import discord
import csv
import io
import schedule
import time
import asyncio
from requests import get
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

#discord variables
target_channel_id = 778792915690323999

@client.event
async def on_ready():
    job1.start()
    job2.start()
    print("CanadaCovid19 Bot is Ready.")

@tasks.loop(hours=24)
async def job1():
    print("Job 1")
    ontario_newcases = get("https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv", verify=False)
    ontario_newcases.encoding = 'utf-8' 
    csvio = io.StringIO(ontario_newcases.text, newline="")
    data = []
    for row in csv.DictReader(csvio):
        data.append(row)
    ontario_newcases.close()
    current_index = len(data)-1
    active_cases = data[current_index]['Confirmed Positive']
    recovered_cases = data[current_index]['Resolved']
    total_deaths = data[current_index]['Deaths']
    total_cases = data[current_index]['Total Cases']
    yesterday_cases = data[current_index-1]['Total Cases']
    new_cases = float(total_cases) - float(yesterday_cases)
    today = date.today()
    date_readable = today.strftime("%B %d, %Y")
    embed=discord.Embed(title="Daily Ontario Covid19 Report", description=date_readable)
    embed.add_field(name="Total Cases", value=total_cases, inline=False)
    embed.add_field(name="Active Cases", value=active_cases, inline=True)
    embed.add_field(name="Recovered Cases", value=recovered_cases, inline=True)
    embed.add_field(name="Total Deaths", value=total_deaths, inline=True)
    embed.add_field(name="New Cases" , value=int(new_cases), inline=True)
    embed.set_footer(text="Developed by The D")
    message_channel = client.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    await message_channel.send(embed=embed)
    await asyncio.sleep(10)

@tasks.loop(hours=24)
async def job2():
    print("Job 2")
    newcases_Region = get("https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_in_cases_by_phu.csv", verify=False)
    newcases_Region.encoding = 'utf-8' 
    csvio = io.StringIO(newcases_Region.text, newline="")
    data2 = []
    for row in csv.DictReader(csvio):
        data2.append(row)
    newcases_Region.close()
    current_index = len(data2)-1
    brantford = data2[current_index]['Brant_County_Health_Unit']
    durham = data2[current_index]['Durham_Region_Health_Department']
    halton = data2[current_index]['Halton_Region_Health_Department']
    hamilton = data2[current_index]['Hamilton_Public_Health_Services']
    niagra = data2[current_index]['Hamilton_Public_Health_Services']
    peel = data2[current_index]['Peel_Public_Health']
    waterloo = data2[current_index]['Region_of_Waterloo,_Public_Health']
    simcoe = data2[current_index]['Simcoe_Muskoka_District_Health_Unit']
    toronto = data2[current_index]['Toronto_Public_Health']
    well_duff_guelph = data2[current_index]['Wellington-Dufferin-Guelph_Public_Health']
    york = data2[current_index]['York_Region_Public_Health_Services']
    today = date.today()
    date_readable = today.strftime("%B %d, %Y")
    embed=discord.Embed(title="Region Statistics - New Cases", description=date_readable)
    embed.add_field(name="Brantford", value=brantford, inline=True)
    embed.add_field(name="Durham", value=durham, inline=True)
    embed.add_field(name="Halton", value=halton, inline=True)
    embed.add_field(name="Hamilton", value=hamilton, inline=True)
    embed.add_field(name="Niagra", value=niagra, inline=True)
    embed.add_field(name="Peel", value=peel, inline=True)
    embed.add_field(name="Waterloo", value=waterloo, inline=True)
    embed.add_field(name="Simcoe", value=simcoe, inline=True)
    embed.add_field(name="Toronto", value=toronto, inline=True)
    embed.add_field(name="Wellington-Dufferin-Guelph", value=well_duff_guelph, inline=True)
    embed.add_field(name="York", value=york, inline=False)
    embed.set_footer(text="Developed by The D")
    message_channel = client.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    await message_channel.send(embed=embed)

client.run(TOKEN)
