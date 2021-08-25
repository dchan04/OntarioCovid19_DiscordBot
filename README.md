# OntarioCovid19_DiscordBot
A Discord bot that reports Covid-19 statistics every 24 hours in a discord server. Only reports certain regions in Ontario. Made purely for friends in discord.

## Building
1. Find and add your discord token to the .env file
2. Open C19.py and replace the variable "target_channel_id" on line 18 with the channel-id of the target discord channel.
3. Run python3 c19.py

## Usage
Every 24 hours from the moment the program runs, Covid-19 statistics from certain regions in Ontario will be posted.
