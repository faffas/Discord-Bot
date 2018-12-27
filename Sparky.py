import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import imdb
import os
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=os.getenv('API_KEY'))
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
	#Movies,TV Series and Video Games plot summaries.
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

#Tech News.
async def send_news():
	await client.wait_until_ready()
	while not client.is_closed:
		th1=newsapi.get_top_headlines(q='tech',sources='engadget',language='en')
		th2=newsapi.get_top_headlines(q='tech',sources='recode',language='en')
		th3=newsapi.get_top_headlines(q='tech',sources='wired',language='en')
		th4=newsapi.get_top_headlines(q='tech',sources='techradar',language='en')
		th5=newsapi.get_top_headlines(q='tech',sources='business-insider',language='en')
		th12=newsapi.get_top_headlines(q='technology',sources='engadget',language='en')
		th22=newsapi.get_top_headlines(q='technology',sources='recode',language='en')
		th32=newsapi.get_top_headlines(q='technology',sources='wired',language='en')
		th42=newsapi.get_top_headlines(q='technology',sources='techradar',language='en')
		th52=newsapi.get_top_headlines(q='technology',sources='business-insider',language='en')
		s=[]
		if (len(th1['articles'])!=0):
			s.append(th1['articles'][0]['url'])
		if (len(th2['articles'])!=0):
			s.append(th2['articles'][0]['url'])
		if (len(th3['articles'])!=0):
			s.append(th3['articles'][0]['url'])
		if (len(th4['articles'])!=0):
			s.append(th4['articles'][0]['url'])
		if (len(th5['articles'])!=0):
			s.append(th5['articles'][0]['url'])
		if (len(th12['articles'])!=0):
			s.append(th12['articles'][0]['url'])
		if (len(th22['articles'])!=0):
			s.append(th22['articles'][0]['url'])
		if (len(th32['articles'])!=0)
			s.append(th32['articles'][0]['url'])
		if (len(th42['articles'])!=0):
			s.append(th42['articles'][0]['url'])
		if (len(th52['articles'])!=0):
			s.append(th52['articles'][0]['url'])
		headlines=list(set(s))
		embed=discord.Embed(title='Tech News',description='The latest Tech News of the day.',colour=discord.Colour.teal())
		embed.set_footer(text='Powered by NewsAPI')
		technews = client.get_channel('523952165526568975')
		if(len(headlines)!=0):
			for i in range(1,len(headlines)+1):
				news_number='News-{}'.format(i)
				embed.add_field(name=news_number,value=headlines[i-1],inline=False)
		else:
			embed.add_field(name='Sorry!',value='No news available right now',inline=False)
		await client.send_message(technews, embed=embed)
		await asyncio.sleep(86400)

client.loop.create_task(send_news())
client.run(os.getenv('TOKEN'))
