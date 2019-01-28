import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import imdb
import os
import random
import wikipedia as wk

ia=imdb.IMDb()
Client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name='with Iron Man.'))
	print("Badum tss, I am ready!")
  
#Commands.
@client.event
async def on_message(message):
	
	#Greetings and Cookies and Random Stuff
	
	if message.content.upper().startswith('HELLO!'):
		userID = message.author.id
		await client.send_message(message.channel,"Hello <@%s>!" % (userID))
	if message.content.upper().startswith('YO!'):
		userID = message.author.id 
		await client.send_message(message.channel,"Yo to you too, <@%s>!" % (userID))
	if message.content.upper().startswith('WAZZ POPPIN!'):
		userID = message.author.id 
		await client.send_message(message.channel,"Not much, <@%s>!" % (userID))
	if message.content.upper().startswith('COOKIE!'):
		cookies=['choco chip','vanilla','caramel','butterscotch','almond','chunky coconut','marmalade','choco lava','butter']
		index_cookie=random.randint(0,len(cookies)-1)
		cookie_send=cookies[index_cookie]
		cookie_message='{} , {} gave you a nice {} cookie :cookie: !'.format(message.content.split(' ')[1],message.author.mention,cookie_send)
		await client.send_message(message.channel, cookie_message)
		
	#Movies,TV Series and Video Games plot summaries
	
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
	
	# 1.) Roles information
	if message.content.upper().startswith('ROLES!'):
		server=client.get_server(os.getenv('SERVER_ID'))
		roles_list=server.role_hierarchy
		for role in roles_list:
			if not role.is_everyone:
				embed=discord.Embed(title=role.name,description='',colour=role.colour)
				await client.send_message(message.channel,embed=embed)
	# 2.) Server information
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
	
	#Moderation Commands

	# 1.) Kick a user
	if message.content.upper().startswith("KICK!"):
		server=client.get_server(os.getenv('SERVER_ID'))
		flag=False
		if message.author.server_permissions.kick_members == True and message.author.server_permissions.ban_members ==  True:
			flag=True
		if flag == True:
			for mem_ber in server.members:
				if mem_ber.mentioned_in(message) ==  True:
					await client.kick(mem_ber)
					embed=discord.Embed(title='Kicked',description="{} has been kicked from the server".format(mem_ber.mention),colour=discord.Colour.red())
					await client.send_message(message.channel,embed=embed)
					break

		else:
			embed=discord.Embed(title='Warning',description='{} You are not allowed to use this command!'.format(message.author.mention),colour=discord.Colour.red())
			await client.send_message(message.channel,embed=embed)
	# 2.) Ban a user
	if message.content.upper().startswith("BAN!"):
		server=client.get_server(os.getenv('SERVER_ID'))
		flag=False
		if message.author.server_permissions.kick_members == True and message.author.server_permissions.ban_members ==  True:
			flag=True
		if flag == True:
			for mem_ber in server.members:
				if mem_ber.mentioned_in(message) ==  True:
					await client.ban(mem_ber,0)
					embed=discord.Embed(title='Banned',description="{} has been banned from the server".format(mem_ber.mention),colour=discord.Colour.red())
					await client.send_message(message.channel,embed=embed)
					break

		else:
			embed=discord.Embed(title='Warning',description='{} You are not allowed to use this command!'.format(message.author.mention),colour=discord.Colour.red())
			await client.send_message(message.channel,embed=embed)


	#Bot Commands Help
	
	if message.content.upper().startswith('HELP!'):
		embed=discord.Embed(title='SPARKY TO YOUR RESCUE!',description='COMMANDS [Note that the commands are case insensitive.] -->',colour=discord.Colour.teal())
		embed.add_field(name='help!',value='Gives the list of commands.',inline=False)
		embed.add_field(name='roles!',value='Gives all the roles present in the server.',inline=False)
		embed.add_field(name='info!',value='Gives server info.',inline=False)
		embed.add_field(name='wiki!',value='Gives brief summary from Wikipedia of the queried item',inline=False)
		embed.add_field(name='coin! type heads or tails',value='Make Sparky toss a coin and see if you win',inline=False)
		embed.add_field(name='slot!',value='Test your luck on Sparky\'s slot machine!',inline=False)
		embed.add_field(name='movie! name of Movie / TV Series /  Video Game',value='Gives the plot summary of the Movie/ TV series / Video Game',inline=False)
		embed.add_field(name='hello! / yo! / wazz poppin!',value='Sparky says hi to you', inline=False)
		embed.add_field(name='cookie! mention user',value='Give someone a delicious cookie', inline=False)
		await client.send_message(message.channel,embed=embed)
		
	#MOD Commands Help

	if message.content.upper().startswith('MODHELP!'):
		if message.author.server_permissions.kick_members == True and message.author.server_permissions.ban_members ==  True:
			embed=discord.Embed(title='MOD COMMANDS',description='Can be used only by Admins.',colour=discord.Colour.red())
			embed.add_field(name='kick! user',value='Kicks the mentioned user from the server.', inline=False)
			embed.add_field(name='ban! user',value='Bans the mentioned user from the server.', inline=False)
			await client.send_message(message.channel,embed=embed)
		else:
			embed=discord.Embed(title='Warning',description='{} You are not allowed to use this command!'.format(message.author.mention),colour=discord.Colour.red())
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
		result=e11+" | "+e12+" | "+e13+"\n"+e21+" | "+e22+" | "+e23+"\n"+e31+" | "+e32+" | "+e33
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

client.run(os.getenv('TOKEN'))
