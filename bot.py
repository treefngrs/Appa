import coc

import discord
from discord.ext import commands

import traceback
import creds
import os
import io

#coc api
coc_client = coc.login(creds.coc_email, creds.coc_password, client=coc.EventsClient, key_names="Appa")

#bot api
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = creds.prefix, intents = intents, case_insensitive=True)
client.coc = coc_client

#cogs
for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		client.load_extension(f"cogs.{file[:-3]}")

@client.event
async def on_ready():
	print(f"{client.user} ready")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title = "Error", description = "No such command", color = 0xf90105)
		await ctx.send(embed = em)
	else:
		raise error

@client.command()
async def this(ctx):
	em = discord.Embed(title = "Appa", description = f'This is {ctx.message.guild.name} server', color = 0x1ef686)
	await ctx.send(embed = em)

@client.command()
async def ping(ctx):
	em = discord.Embed(title = "Appa", description = f'Ping: {round(client.latency * 1000)}ms', color = 0x1ef686)
	await ctx.send(embed = em)

async def is_owner(ctx):
    return ctx.author.id == creds.author

@client.command()
@commands.check(is_owner)
async def refresh(ctx, extension='all'):
	if extension=="all":
		for file in os.listdir("./cogs"):
			if file.endswith(".py"):
				client.unload_extension(f"cogs.{file[:-3]}")
				client.load_extension(f"cogs.{file[:-3]}")
		em = discord.Embed(title = "Appa", description = 'Cogs reloaded', color = 0x1ef686)
		await ctx.send(embed = em)
		return
	if extension+".py" in os.listdir("./cogs"):
		client.unload_extension(f"cogs.{extension}")
		client.load_extension(f"cogs.{extension}")
		em = discord.Embed(title = "Appa", description = f'{extension} extension reloaded', color = 0x1ef686)
		await ctx.send(embed = em)
		return
	em = discord.Embed(title = "Error", description = f'og not found', color = 0xf90105)
	await ctx.send(embed = em)

#help command 
client.remove_command("help")

@client.group(invoke_without_command=True)
async def help(ctx):
	em = discord.Embed(title = "Help", description = f"{creds.prefix}help <command> for specific command info", color = 0x1ef686)
	em.add_field(name = "General", value = "clan, members, th, war")
	em.add_field(name = "SCCWL", value = "league, lotto")
	em.add_field(name = "MLCW", value = "mr, inc, missing, lineup, abbs, subs")

	await ctx.send(embed = em)

@help.command()
async def clan(ctx):
	em = discord.Embed(title = "Clan", description = "Displays clan's information", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}clan [tag]\n```")

	await ctx.send(embed = em)

@help.command()
async def members(ctx):
	em = discord.Embed(title = "Members", description = "Displays a clan's member list", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}members [tag]\n```")

	await ctx.send(embed = em)

@help.command()
async def th(ctx):
	em = discord.Embed(title = "TH", description = "Displays a clan's TH member list", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}th [lvl]\n```")

	await ctx.send(embed = em)

@help.command()
async def war(ctx):
	em = discord.Embed(title = "War", description = "Displays a clan's current war info", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}war [tag]\n```")

	await ctx.send(embed = em)

@help.command()
async def league(ctx):
	em = discord.Embed(title = "League", description = "Displays a clan's current clan war league's member list", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}league [tag]\n```")

	await ctx.send(embed = em)

@help.command()
async def lotto(ctx):
	em = discord.Embed(title = "Lotto", description = "Picks n winners for SCCWL medals from the home clan pool", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}lotto\n```")

	await ctx.send(embed = em)

@help.command()
async def mr(ctx):
	em = discord.Embed(title = "MR", description = "Displays a clan's BKL MR", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}mr [abb] [TH lvl]\n```")

	await ctx.send(embed = em)

@help.command()
async def inc(ctx):
	em = discord.Embed(title = "In Clan", description = "Displays the list of MR players in clan", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}clan [tag]\n```")

	await ctx.send(embed = em)

@help.command()
async def missing(ctx):
	em = discord.Embed(title = "Missing", description = "Displays the list of missing players in clan for a league match", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}missing [week]\n```")

	await ctx.send(embed = em)

@help.command()
async def lineup(ctx):
	em = discord.Embed(title = "Lineup", description = "Displays the lineup for a certain week's match", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}lineup [week]\n```")

	await ctx.send(embed = em)

@help.command()
async def abbs(ctx):
	em = discord.Embed(title = "Abbreviations", description = "Displays the abbreviations list for BKL", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}abbs\n```")

	await ctx.send(embed = em)

@help.command()
async def subs(ctx):
	em = discord.Embed(title = "Subs", description = "Displays the list of subs an opponent is using", color = 0x1ef686)
	em.add_field(name = "Usage", value = f"```\n{creds.prefix}subs [abb]\n```")

	await ctx.send(embed = em)

client.run(creds.bot_token)