import os
import discord
import csv
import io
from requests import get
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

#discord variables
target_channel_id = 778792915690323999

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
new_cases = int(total_cases) - int(yesterday_cases)
#total_tests = data[current_index]['Total tests completed in the last day']
#percent_positive = data[current_index]['Percent positive tests in last day']
#new_cases = int(total_tests) * (float(percent_positive)/100)
print(active_cases)
print(recovered_cases)
print(total_deaths)
print(total_cases)
print(yesterday_cases)
print(new_cases)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    response = get("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv", verify=False)
    response.encoding = 'utf-8' 
    csvio = io.StringIO(response.text, newline="")
    data = []
    for row in csv.DictReader(csvio):
        data.append(row)
    response.close()
    
    #newCases_Today = data[len(data)-1]['numtoday']
    #deaths_Today = data[len(data)-1]['numdeathstoday']
    #recovered_Today = data[len(data)-1]['numrecoveredtoday']
    #embed = discord.Embed(title="Daily Covid19 Report", description="Ontario Only Statistics") #,color=Hex code
    #embed.add_field(name="New Cases Today", value=newCases_Today)
    #embed.add_field(name="Deaths Today", value=deaths_Today)
    #embed.add_field(name="Recovered Today", value=recovered_Today)
    #embed.set_footer(text="Developed by The D")
    #message_channel = client.get_channel(target_channel_id)
    #print(f"Got channel {message_channel}")
    #await message_channel.send(embed=embed)

#client.run(TOKEN)


#Total 
#total_Deaths = data[len(data)-1]['numtotal']
#total_Recovered = data[len(data)-1]['numrecover']

#Today
#newCases_Today = data[len(data)-1]['numtoday']
#deaths_Today = data[len(data)-1]['numdeathstoday']
#recovered_Today = data[len(data)-1]['numrecoveredtoday']

#Last 14 Days
#newCases_Last14 = data[len(data)-1]['numtotal_last14']
#newDeaths_Last14 = data[len(data)-1]['numdeaths_last14']

#Last 7 Days
#newCases_Last7 = data[len(data)-1]['numtotal_last7']
#newDeaths_Last7 = data[len(data)-1]['numdeaths_last7']
