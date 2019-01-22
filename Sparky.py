import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import imdb
import os
import random
import wikipedia as wk
# from newsapi import NewsApiClient

# newsapi = NewsApiClient(api_key=os.getenv('API_KEY'))
# The tech news feature can be enabled by using an API. I am trying to create it using a RSS Feed. It will be updated soon.

ia=imdb.IMDb()
Client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name='with Iron Man.'))
	print("Badum tss, I am ready!")
  
#Greeting someone when the user says !hello,!yo and !wazz poppin/ Movies Bot integration.
@client.event
async def on_message(message):
	#Greetings.
	if message.content.upper().startswith('HELLO!'):
		userID = message.author.id
		await client.send_message(message.channel,"Hello <@%s>!" % (userID))
	if message.content.upper().startswith('YO!'):
		userID = message.author.id 
		await client.send_message(message.channel,"Yo to you too, <@%s>!" % (userID))
	if message.content.upper().startswith('WAZZ POPPIN!'):
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
		embed=discord.Embed(title='PLOT SUMMARY',description='',colour=discord.Colour.teal())
		embed.add_field(name=moviename,value=plot,inline=False)
		await client.send_message(message.channel,embed=embed)
		
	#Wikipedia Search
	if message.content.upper().startswith('WIKI!'):
		args = message.content.split(" ")
		item_search_title=" ".join(args[1:])
		item_summary=wk.summary(item_search_title,sentences=4)
		embed=discord.Embed(title='Wikipedia Summary',description='',colour=discord.Colour.teal())
		embed.add_field(name=item_search_title.capitalize(),value=item_summary,inline=False)
		await client.send_message(message.channel,embed=embed)
	
	#Server Info
		#Roles information
	if message.content.upper().startswith('ROLES!'):
		server=client.get_server(os.getenv('SERVER_ID'))
		roles_list=server.role_hierarchy
		for role in roles_list:
			if not role.is_everyone:
				embed=discord.Embed(title=role.name,description='',colour=role.colour)
				await client.send_message(message.channel,embed=embed)
		#Server information
	if message.content.upper().startswith('INFO!'):
		server=client.get_server(os.getenv('SERVER_ID'))
		people_count=server.member_count
		time_of_creation=server.created_at
		owner_name=server.owner.name
		icon=server.icon_url
		embed=discord.Embed(title=server.name,description='SERVER INFO',colour=discord.Colour.teal())
		embed.set_image(url=icon)
		embed.add_field(name='Member count:',value=people_count,inline=False)
		embed.add_field(name='Time of Origin:',value=time_of_creation,inline=False)
		embed.add_field(name='Owner:',value=owner_name,inline=False)
		await client.send_message(message.channel,embed=embed)

	#Bot Commands Help
	if message.content.upper().startswith('HELP!'):
		embed=discord.Embed(title='Sparky to your rescue!',description='COMMANDS [Note that the commands are case insensitive.] -->',colour=discord.Colour.teal())
		embed.add_field(name='help!',value='Gives the list of commands.',inline=False)
		embed.add_field(name='roles!',value='Gives all the roles present in the server.',inline=False)
		embed.add_field(name='info!',value='Gives server info.',inline=False)
		embed.add_field(name='coin! type heads or tails',value='Make Sparky toss a coin and see if you win',inline=False)
		embed.add_field(name='slot!',value='Test your luck on Sparky\'s slot machine!',inline=False)
		embed.add_field(name='wiki! what you want to search',value='Gives brief summary from Wikipedia of the queried item.',inline=False)
		embed.add_field(name='movie! name of Movie / TV Series /  Video Game',value='Gives the plot summary of the Movie/ TV series / Video Game.',inline=False)
		embed.add_field(name='hello! / yo! / wazz poppin!',value='Sparky says hi to you!', inline=False)
		await client.send_message(message.channel,embed=embed)
	
	#Coin Flip Game
	if message.content.upper().startswith('COIN!'):
		args=message.content.split(" ")
		result_list=["Heads","Tails"]
		choice=random.randint(0,1)
		if args[1].upper()==result_list[choice].upper():
			result="{} it is! You win!".format(result_list[choice])
			embed=discord.Embed(title='Coin Flip',description=result,colour=discord.Colour.teal())
			await client.send_message(message.channel,embed=embed)
		else:
			result=" Uh oh, its {}! Better luck next time!".format(result_list[choice])
			embed=discord.Embed(title='Coin Flip',description=result,colour=discord.Colour.teal())
			await client.send_message(message.channel,embed=embed)

	#Slot Machine Game
	if message.content.upper().startswith('SLOT!'):
		result_list=[':apple:',':pear:',':tangerine:']
		result_list2=[':grapes:',':strawberry:',':cherries:']
		result_list3=[':hotdog:',':icecream:',':taco:']
		choice1=random.randint(0,2)
		choice2=random.randint(0,2)
		choice3=random.randint(0,2)
		e11=result_list[choice1]
		e12=result_list[choice2]
		e13=result_list[choice3]
		e21=result_list2[choice1]
		e22=result_list2[choice2]
		e23=result_list2[choice3]
		e31=result_list3[choice1]
		e32=result_list3[choice2]
		e33=result_list3[choice3]
		result=e11+" | "+e12+" | "+e13+" | "+"\n"+e21+" | "+e22+" | "+e23+" | "+"\n"+e31+" | "+e32+" | "+e33+" | "
		row1=False
		row2=False
		row3=False
		row_count=0
		if (e11==e12) and (e12==e13) and (e13==e11):
			row1=True
			row_count+=1
		if (e21==e22) and (e22==e23) and (e23==e21):
			row2=True
			row_count+=1
		if (e31==e32) and (e32==e33) and (e33==e31):
			row3=True
			row_count+=1
		if row_count==0:
			res_mes="Better luck next time!"
		if row_count==1:
			res_mes="You got 1 row! Nice work!"
		if row_count==2:
			res_mes="You got 2 rows! Awesome!"
		if row_count==3:
			res_mes="Hattrick!"
		embed=discord.Embed(title='Slot Machine',description=result,colour=discord.Colour.teal())
		embed.add_field(name='Result',value=res_mes, inline=False)
		await client.send_message(message.channel,embed=embed)


#Introduction of a new user. Note that in asyncio the ids are strings.	
@client.event
async def on_member_join(member):
	userid=member.mention
	channel = client.get_channel(os.getenv('INTRO_CHANNEL_ID'))
	channel_rules=client.get_channel(os.getenv('RULES_CHANNEL_ID'))
	msg='Welcome to Sparks and Glory {}! Please look at {} before proceeding. Have fun!'.format(userid,channel_rules.mention)
	await client.send_message(channel,msg)

#Bidding goodbye when a member leaves.
@client.event
async def on_member_remove(member):
	userid=member.mention
	channel=client.get_channel(os.getenv('INTRO_CHANNEL_ID'))
	msg='Farewell {}! Best of luck for the future!'.format(userid)
	await client.send_message(channel,msg)

# #Tech News.
# async def send_news():
# 	await client.wait_until_ready()
# 	while not client.is_closed:
# 		th1=newsapi.get_top_headlines(q='tech',sources='engadget',language='en')
# 		th2=newsapi.get_top_headlines(q='tech',sources='recode',language='en')
# 		th3=newsapi.get_top_headlines(q='tech',sources='wired',language='en')
# 		th4=newsapi.get_top_headlines(q='tech',sources='techradar',language='en')
# 		th12=newsapi.get_top_headlines(q='technology',sources='engadget',language='en')
# 		th22=newsapi.get_top_headlines(q='technology',sources='recode',language='en')
# 		th32=newsapi.get_top_headlines(q='technology',sources='wired',language='en')
# 		th42=newsapi.get_top_headlines(q='technology',sources='techradar',language='en')
# 		s=[]
# 		if (len(th1['articles'])!=0):
# 			s.append(th1['articles'][0]['url'])
# 		if (len(th2['articles'])!=0):
# 			s.append(th2['articles'][0]['url'])
# 		if (len(th3['articles'])!=0):
# 			s.append(th3['articles'][0]['url'])
# 		if (len(th4['articles'])!=0):
# 			s.append(th4['articles'][0]['url'])
# 		if (len(th12['articles'])!=0):
# 			s.append(th12['articles'][0]['url'])
# 		if (len(th22['articles'])!=0):
# 			s.append(th22['articles'][0]['url'])
# 		if (len(th32['articles'])!=0):
# 			s.append(th32['articles'][0]['url'])
# 		if (len(th42['articles'])!=0):
# 			s.append(th42['articles'][0]['url'])
# 		headlines=list(set(s))
# 		embed=discord.Embed(title='Tech News',description='Stuff happening in the Tech World. ',colour=discord.Colour.teal())
# 		embed.set_footer(text='Powered by NewsAPI')
# 		technews = client.get_channel(os.getenv('TECHNEWS_CHANNEL_ID'))
# 		if(len(headlines)!=0):
# 			for i in range(1,len(headlines)+1):
# 				news_number='News-{}'.format(i)
# 				embed.add_field(name=news_number,value=headlines[i-1],inline=False)
# 		else:
# 			embed.add_field(name='Sorry!',value='No news available right now',inline=False)
# 		await client.send_message(technews, embed=embed)
# 		await asyncio.sleep(345600)

# client.loop.create_task(send_news())
client.run(os.getenv('TOKEN'))
