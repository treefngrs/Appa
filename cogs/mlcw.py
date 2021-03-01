import discord
from discord.ext import commands
import coc
from googleapiclient.discovery import build
from google.oauth2 import service_account

import creds
import tools as ts

#sheets api
SCOPES = [creds.scopes]
SERVICE_ACCOUNT_FILE = creds.service_account_file

google_creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=google_creds)

MASTERROSTER = creds.mr
DASHBOARD = creds.dashboard

ABBS = ts.parseList('clanList.csv') 

async def totalmr(ctx, team):
	name = ts.abb2name(ts.acabb(team, ABBS), ABBS)
	if name is None:
		em = discord.Embed(title = "Error", description = f'```\nNo such clan with abbreviation \'{team}\'\n```', color = 0xf90105)
		await ctx.send(embed = em)
		return

	values = ts.loadMR(ts.acabb(team, ABBS), MASTERROSTER, service)

	bd = [0, 0, 0]

	template = '{2:5} {0:12} {1:21}'

	mr = f'= TH    Tag          Name =\n'
	for val in values:
		if val[2] == '13':
			bd[0] = bd[0] + 1
		if val[2] == '12':
			bd[1] = bd[1] + 1
		if val[2] == '11':
			bd[2] = bd[2] + 1
		mr = mr + '\n  ' + template.format(*val)

	em = discord.Embed(title = f"- {name} MR", description = f'```asciidoc\n{mr}\n```', color = 0x1ef686)
	em.add_field(name = "BD", value = "```asciidoc\n[ " + '{0}/{1}/{2}'.format(*bd) + ' | ' + str(sum(bd)) +' total accounts ]\n```')

	await ctx.send(embed = em)

async def thmr(ctx, th, team):
	name = ts.abb2name(ts.acabb(team, ABBS), ABBS)
	if name is None:
		em = discord.Embed(title = "Error", description = f'```\nNo such clan with abbreviation \'{team}\'\n```', color = 0xf90105)
		await ctx.send(embed = em)
		return

	values = ts.loadMR(ts.acabb(team, ABBS), MASTERROSTER, service)
	count = 0
	template = '{2:5} {0:12} {1:21}'

	mr = '= TH    Tag          Name =\n'
	for val in values:
		if val[2] == th:
			count = count + 1
			mr = mr + '\n  ' + template.format(*val)

	if count == 0:
		em = discord.Embed(title = "Error", description = '```\nNo accounts with such TH level\n```', color = 0xf90105)
		await ctx.send(embed = em)
	else:
		em = discord.Embed(title = f"- {name} TH{th} MR", description = f'```asciidoc\n{mr}\n\n[ ' + str(count) + ' accounts ]\n```', color = 0x1ef686)
		await ctx.send(embed = em)


class Mlcw(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('mlcw.py ready')

	@commands.command(aliases=['master', 'masterroster', 'roster'])
	async def mr(self, ctx, *args):
		if len(args) == 0:
			await totalmr(ctx, creds.abb)
		elif len(args) == 1:
			if ts.isInt(args[0]):
				await thmr(ctx, args[0], creds.abb)
			else:
				await totalmr(ctx, args[0])
		elif len(args) == 2 and ts.isInt(args[0])==False and ts.isInt(args[1]):
			await thmr(ctx, args[1], args[0])
		else:
			em = discord.Embed(title = "Error", description = f'```\nTry {creds.prefix}help mr\n```', color = 0xf90105)
			await ctx.send(embed = em)
			
	@commands.command()
	async def abbs(self, ctx):
		cad = ''
		for k in ABBS.keys():
			cad += f' {k} : {ABBS[k][0]}\n'
		em = discord.Embed(title = "- MLCW BKL Abbreviations", description = f'```\n{cad}```', color = 0x1ef686)
		await ctx.send(embed = em)

	@commands.command()
	async def lineup(self, ctx, week):
		values = None
		values = ts.loadRoster(week, DASHBOARD, service)

		bd = [0] * 3

		template = '{2:5} {0:12} {1:21}'
		mr = '= TH    Tag          Name =\n'

		for val in values:
			if val[2] == '13':
				bd[0] = bd[0] + 1
			if val[2] == '12':
				bd[1] = bd[1] + 1
			if val[2] == '11':
				bd[2] = bd[2] + 1

			mr = mr + '\n  ' + template.format(*val)

		em = discord.Embed(title = f'- {creds.clan_name} Week {week[1:]} Roster', description = f'```asciidoc\n{mr}\n```', color = 0x1ef686)
		em.add_field(name = "BD", value = "```asciidoc\n[ " + '{0}/{1}/{2}'.format(*bd) + ' | ' + str(sum(bd)) +' total accounts ]\n```')

		await ctx.send(embed = em)

	@commands.command()
	async def inc(self, ctx, event='no'):
		values = ts.loadMR(creds.abb, MASTERROSTER, service)

		if event == 'no':
			clan_tag = creds.clan_tag
			clan_name = creds.clan_name
		elif event == 'event':
			clan_tag = creds.second_tag
			clan_name = creds.second_name
		else:
			em = discord.Embed(title = "Error", description = f'```\nInvalid argument\n```', color = 0xf90105)
			await ctx.send(embed = em)

		if event == 'no' or event == 'event':
			empty = 1
			clan = await self.client.coc.get_clan(clan_tag)
			members = clan.members

			bd = [0] * 3

			finder = None
			cad = '= TH    Tag          Name =\n'
			template = '{2:5} {0:12} {1:21}'

			for val in values:
				finder = coc.utils.get(members, tag = val[0])
				if finder != None:
					if val[2] == '13':
						bd[0] = bd[0] + 1
					elif val[2] == '12':
						bd[1] = bd[1] + 1
					elif val[2] == '11':
						bd[2] = bd[2] + 1
					empty = 0
					cad = cad + f'\n  {template.format(*val)}'
			if empty:
				em = discord.Embed(title = " No MR accounts in clan", description = f'```\nFound 0 rostered accounts in {clan_name}\n```', color = 0xf90105)
				await ctx.send(embed = em)
			else:
				em = discord.Embed(title = f"- MR accounts in {clan_name}", description = f'```asciidoc\n{cad}\n```', color = 0x1ef686)
				em.add_field(name = "BD", value = "```asciidoc\n[ " + '{0}/{1}/{2}'.format(*bd) + ' | ' + str(sum(bd)) +' total accounts ]\n```')

				await ctx.send(embed = em)

				#await ctx.send(f'```asciidoc\n- AW MR accounts in {clan_name}\n\n= TH    Tag          Name =\n{cad}\n\n[ BD: ' + '{0}/{1}/{2}'.format(*bd) + ' | ' + str(sum(bd)) +' total accounts ]\n```')

	@commands.command()
	async def missing(self, ctx, *args):
		clan_tag = ''
		name = ''
		if len(args) == 2 and args[1]=='event':
			clan_tag = creds.second_tag
			name = creds.second_name
		elif len(args) != 1:
			em = discord.Embed(title = "Error", description = f"Wrong arguments. Try {creds.prefix}help missing", color = 0xf90105)
			await ctx.send(embed = em)
			return
		else:
			clan_tag = creds.clan_tag
			name = creds.clan_name
		week = args[0]
		empty = True
		values = ts.loadRoster(week, DASHBOARD, service)
		mia = f'```\n'
		player = None
		template = '{2:5} {0:12} {1:21}'
		for val in values:
			player = await self.client.coc.get_player(val[0])
			if not player.clan is None and player.clan.tag != clan_tag:
				empty = False
				mia += f'\n  {template.format(*val)}'
		if empty:
			mia += "\n No players missing"
		em = discord.Embed(title = f"- Missing Week {week[1:]} players in {name}", description = mia+'\n```', color = 0x1ef686)
		await ctx.send(embed = em)

	@commands.command()
	async def subs(self, ctx, *args):
		clan_tag = ''
		if len(args) == 2 and args[1]=='event':
			clan_tag = creds.second_tag
		elif len(args) != 1:
			em = discord.Embed(title = "Error", description = f"```\nWrong arguments. Try {creds.prefix}help subs\n```", color = 0xf90105)
			await ctx.send(embed = em)
			return
		else:
			clan_tag = creds.clan_tag
		war = await self.client.coc.get_clan_war(clan_tag)
		abb = ts.acabb(args[0], ABBS)
		if abb is None:
			em = discord.Embed(title = "Abbreviation unrecognised", description = f"Check the full list by doing {creds.prefix}abbs", color = 0xf90105)
			await ctx.send(embed = em)
			return
		name = ts.abb2name(abb, ABBS)
		if war.opponent.tag != ts.abb2clan(abb, ABBS) and war.opponent.tag != ts.abb2event(abb, ABBS):
			em = discord.Embed(title = f"Not in war against {name}", description = f"Make sure that's the current opponent", color = 0xf90105)
			await ctx.send(embed = em)
			return
		opp = war.opponent.members
		ls = ts.loadMR(abb, MASTERROSTER, service)
		noSubs = True
		cad = f'```diff\n- Subs in {name}\n'
		for mem in opp:
			if mem.tag not in [a[0] for a in ls]:
				cad += f'\n  {mem.town_hall:5} {mem.tag:12} {mem.name:21}'
				noSubs = False
		if noSubs:
			em = discord.Embed(title = "No subs found", description = f"{name} is using all rostered players", color = 0x1ef686)
			await ctx.send(embed = em)
			return
		await ctx.send(cad+'\n```')

def setup(client):
	client.add_cog(Mlcw(client))