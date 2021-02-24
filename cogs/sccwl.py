import discord
from discord.ext import commands
import coc
import creds
import tools as ts

class Sccwl(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('sccwl.py ready')

	@commands.command()
	async def league(self, ctx, clan_tag = creds.clan_tag):
		league = await self.client.coc.get_league_group(clan_tag)
		if league is None:
			em = discord.Embed(title = "Error", description = "The clan isn't in SCCWL right now", color = 0xf90105)
			await ctx.send(embed = em)
			return
		members = None
		name = ''

		for clan in league.clans:
			if clan.tag == coc.utils.correct_tag(clan_tag):
				members = clan.members
				name = clan.name
				break

		bd = [0] * 4
		total = len(members)

		template = '{2:5} {0:12} {1:21}'
		mr = f'asciidoc\n= TH    Tag          Name =\n'
		for mem in members:
			if mem.town_hall == 13:
				bd[0] += 1
			elif mem.town_hall == 12:
				bd[1] += 1
			elif mem.town_hall == 11:
				bd[2] += 1
			else:
				bd[3] += 1
			mr = mr +'\n  ' + template.format(str(mem.tag), mem.name, str(mem.town_hall))
		await ctx.send(f'```{mr}```')

		em = discord.Embed(title = f"{name} SCCWL members list", description = f'```asciidoc\n{mr}\n```', color = 0x1ef686)
		em.add_field(name = "BD", value = "```asciidoc\n[ " + '{0}/{1}/{2}/../{3}'.format(*bd) + ' | ' + str(total) +' total accounts ]\n```')

		await ctx.send(embed = em)

	@commands.command()
	async def lotto(self, ctx, n = 3):
		league = await self.client.coc.get_league_group(creds.clan_tag)
		if league is None:
			em = discord.Embed(title = "Error", description = "The clan isn't in SCCWL right now", color = 0xf90105)
			await ctx.send(embed = em)
			return
		members = None
		name = ''
		if n < 1:
			em = discord.Embed(title = "Error", description = f'```\nInvalid amount of bonuses\n```', color = 0xf90105)
			await ctx.send(embed = em)
			return
		
		for clan in league.clans:
			if clan.tag == creds.clan_tag:
				members = clan.members
				name = clan.name
				break

		if n > len(members):
			em = discord.Embed(title = "Error", description = f'```\nToo many bonuses\n```', color = 0xf90105)
			await ctx.send(embed = em)
			return
		cad = ''
		winners = ts.urng(n, len(members))
		for w in winners:
			cad += f' {members[w]}\n'
		em = discord.Embed(title = f"SCCWL bonuses winners", description = f'```\n{cad}\n```', color = 0x1ef686)
		await ctx.send(embed = em)

def setup(client):
	client.add_cog(Sccwl(client))