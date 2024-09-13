import discord
from discord.ext import commands
from random import randint

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True 
intents.message_content = True

global JoueursID
global partie
global JoueursName
global JoueursRole
global Membres
Membres=[]
JoueursRole=[]
JoueursName=[]
JoueursID =[]
partie=0
bot = commands.Bot(command_prefix="/", description="Bot pour jouer aux loup-garou", intents=intents)

@bot.event
async def on_ready():
	print("Bot prêt")

@bot.command()
async def lgnew(ctx, nombreDeJoueurs: int = 0, numeroDeConfig: int = 0):
	global nombreJoueurs
	global numeroConfig
	nombreJoueurs=nombreDeJoueurs
	numeroConfig=numeroDeConfig
	if nombreJoueurs==0:
		await ctx.send("combien de joueurs êtes vous ?\nLance la partie avec =lgnew <nombre_de_joueurs>")	
	elif numeroConfig==0:	
		await ctx.send("quelle configuration voulez vous ?\nRegarde les config avec =lgconfig <nombre_de_joueurs>\nLance la partie avec =lgnew <nombre_de_joueurs> <Numero_de_la_config>")
	else:
		strNombreJoueurs=str(nombreJoueurs)
		strNumeroConfig=str(numeroConfig)
		message = await ctx.send(f"attente de joueurs pour débuter la partie\n Quand tout les joueurs sont prêts lancez la partie avec =lgstart")
		await message.add_reaction("✅")
	def checkEmoji(reaction, user):
		if (753000637255647352 != user.id and (str(reaction.emoji) == "✅")):
			a=1
			for k in range(len(JoueursID)):
				if JoueursID[k]==user.id:
					a=0
			if a==1:
				JoueursID.append(user.id)
				JoueursName.append(user.name)
				Membres.append(user)

				return True
			else:
				return False
	for k in range(nombreJoueurs):
		reaction, user = await bot.wait_for("reaction_add", check = checkEmoji)
		print("ok")
		if reaction.emoji == "✅":
			NomJoueurs=str(JoueursID[k])
			NomJoueurs="<@"+NomJoueurs+">"
			message=(NomJoueurs," est prêt pour la partie de loup-garou")
			await ctx.send("".join(message))
@bot.command()
async def lgstart(ctx):
	guild=ctx.guild
	def OccurenceListe(liste,a):
		if liste[a]==0:
			return 0
		else:
			return 1
	if nombreJoueurs==len(JoueursID):
		partie=1 
	else:
		partie=0
	if partie == 1:
		await ctx.send("lancement de la partie")
		if nombreJoueurs==4:
			c=0
			d=0
			for k in range(nombreJoueurs):
				JoueursRole.append(0)
			if numeroConfig==1:
				a=1
				for k in range(nombreJoueurs):
					x=randint(1,4)
					x=x-1
					fin=0
					while fin==0:
						if JoueursRole[x]==0:
							if a==1:
								JoueursRole[x]=1
								a=2
								fin=1
							elif a==2:
								JoueursRole[x]=2
								fin=1
						else:
							x=randint(1,4)
							x=x-1
				for k in range(nombreJoueurs):
					if JoueursRole[k]==1:
						await Membres[k].send("tu es loup-garou")
					elif JoueursRole[k]==2:
						await Membres[k].send("tu es villageois")
			counterLG=0
			counterVillage=0
			NomCategorie=0
			channelLG=0
			for Channel in guild.channels:
				StrChannel=str(Channel)
				if StrChannel=="Loup-garou":
					NomCategorie=Channel
				if StrChannel=="loup-garou":
					counterLG=1
					guild=ctx.guild
					channel = discord.utils.get(guild.text_channels, name=StrChannel)
					channelLG=channel
					async for msg in channel.history():
						await msg.delete()
				
				if StrChannel=="village":
					counterVillage=1
					guild=ctx.guild
					channel = discord.utils.get(guild.text_channels, name=StrChannel)
					async for msg in channel.history():
						await msg.delete()
			if NomCategorie==0 : 
				await guild.create_category("Loup-garou")
				for Channel in guild.channels:
					StrChannel=str(Channel)
					if StrChannel=="Loup-garou":
						NomCategorie=Channel				
			if counterVillage==0 :
				
				overwrites = {
				    guild.default_role: discord.PermissionOverwrite(read_messages=True)
				}

				channel = await guild.create_text_channel('village', overwrites=overwrites)
				channel = await channel.edit(category=NomCategorie)
			if counterLG==0:
				channel = await guild.create_text_channel('loup-garou')
			
			overwrites = {
			    guild.default_role: discord.PermissionOverwrite(read_messages=False)		    	
			}
			channel = await channel.edit(category=NomCategorie, overwrites=overwrites)
			loupGarou1=0
			for k in range(len(JoueursRole)):
				if JoueursRole[k]==1:
					loupGarou1=Membres[k]
			await channelLG.set_permissions(loupGarou1,read_messages=True,send_messages=True)
			await channelLG.send("Ceci est le channel pour voter et pour discuter avec tes camarades loup-garous si tu en a :)")
@bot.command()
async def lgstop(ctx):
	Membres=[]
	JoueursRole=[]
	JoueursName=[]
	JoueursID =[]
	partie=0
	nombreJoueurs=0
@bot.command()
async def cmdclean(ctx,texte:str):
	guild=ctx.guild
	channel = discord.utils.get(guild.text_channels, name=texte)
	async for msg in channel.history():
		await msg.delete()
@bot.command()
async def clean(ctx):
	channel=ctx.channel
	guild=ctx.guild
	async for msg in channel.history():
		await msg.delete()


"""
@bot.command()
async def newchannel(ctx):
	guild=ctx.guild
	await guild.create_text_channel("test")
@bot.command()
async def supprchannel(ctx):
	await 755501582992277656.delete()
"""

@bot.command()
async def lgconfig(ctx,nombre_Joueurs:int=0):
	if nombre_Joueurs<4:
		await ctx.send("le nombre de joueurs minimal est 4 écrivez sous la forme de:\n=lgconfig <nombre_de_joueurs>")
	elif nombre_Joueurs>12:
		await ctx.send("le nombre de joueurs maximal est 12")
	else:
		if nombre_Joueurs==4:
			await ctx.send("La config n°1 pour 4 joueurs est:\n1 Loup-garou\n3 villageois") 
		elif nombre_Joueurs==5:
			await ctx.send("La config n°1 pour 5 joueurs est:\n1 Loup-garou\n4 villageois")
		elif nombre_Joueurs==6:
			await ctx.send("La config n°1 pour 6 joueurs est:\n1 Loup-garou\n5 villageois") 
		elif nombre_Joueurs==7:
			await ctx.send("La config n°1 pour 7 joueurs est:\n2 Loup-garou\n5 villageois") 
		elif nombre_Joueurs==8:
			await ctx.send("La config n°1 pour 8 joueurs est:\n2 Loup-garou\n6 villageois") 
		elif nombre_Joueurs==9:
			await ctx.send("La config n°1 pour 9 joueurs est:\n2 Loup-garou\n7 villageois") 
		elif nombre_Joueurs==10:
			await ctx.send("La config n°1 pour 10 joueurs est:\n3 Loup-garou\n7 villageois") 
		elif nombre_Joueurs==11:
			await ctx.send("La config n°1 pour 11 joueurs est:\n3 Loup-garou\n8 villageois") 
		elif nombre_Joueurs==12:
			await ctx.send("La config n°1 pour 12 joueurs est:\n3 Loup-garou\n9 villageois") 


@bot.command()
async def say(ctx, *texte):
	await ctx.send(" ".join(texte))


	
bot.run("clé du bot discord") 
