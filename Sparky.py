import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import imdb
import os

ia=imdb.IMDb()
Client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
	print("Badum tss, I am ready!")
  
#Greeting someone when the user says !hello,!yo and !wazz poppin/ Movies Bot integration.
@client.event
async def on_message(message):
	#Greetings.
	if message.content.upper().startswith('!HELLO'):
		userID = message.author.id 
		await client.send_message(message.channel,"Hello <@%s>!" % (userID))
	if message.content.upper().startswith('!YO'):
		userID = message.author.id 
		await client.send_message(message.channel,"Yo to you too, <@%s>!" % (userID))
	if message.content.upper().startswith('!WAZZ POPPIN?'):
		userID = message.author.id 
		await client.send_message(message.channel,"Not much, <@%s>!" % (userID))
	#Movies.
	if message.content.upper().startswith('MOVIE!'):
		userID = message.author.id 
		args = message.content.split(" ")
		moviename=" ".join(args[1:])
		movie=ia.search_movie(moviename)
		movie1=movie[0]
		movieid=ia.get_imdbID(movie1)
		movieinfo=ia.get_movie(movieid)
		plot=movieinfo['plot'][0]
		await client.send_message(message.channel,plot)


#Introduction of a new user. Note that in asyncio the ids are strings.	
@client.event
async def on_member_join(member):
	userid=member.mention
	channel = client.get_channel('523991595494932491')
	channel_rules=client.get_channel('519140177512366082')
	msg='Welcome to Sparks and Glory {}! Please look at {} before proceeding. Have fun!'.format(userid,channel_rules.mention)
	await client.send_message(channel,msg)

client.run(os.getenv('TOKEN'))
