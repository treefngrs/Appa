import discord
from discord.ext import commands
import coc
import creds
import tools as ts

class General(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('general.py ready')

	@commands.command()
	async def war(self, ctx, clan_tag=creds.clan_tag):
		war = await self.client.coc.get_clan_war(clan_tag)
		if war is None:
			print("War not found")
			return
		cad = ""
		if war.state=="preparation":
			time = ts.s2h(war.start_time.seconds_until)
			cad = f"Preparation day - War starts in {time}"
		elif war.state=="inWar":
			time = ts.s2h(war.end_time.seconds_until)
			cad = f"In war - War ends in {time}"
		elif war.state=="warEnded":
			cad = f"War ended - {war.clan} {war.status}"
		em = discord.Embed(title=f"{war.clan} vs {war.opponent}", description=cad, color=0x1ef686)
		await ctx.send(embed = em)

	@commands.command(name="members", aliases=["get_members"])
	async def members(self, ctx, clan_tag=creds.clan_tag):

		clan_tag = coc.utils.correct_tag(clan_tag)

		clan = await self.client.coc.get_clan(clan_tag)
		total = clan.member_count

		bd = [0] * 4

		template = "{2:5} {0:12} {1:21}"
		mr = "= TH    Tag          Name =\n"
		async for mem in clan.get_detailed_members():
			if mem.town_hall == 13:
				bd[0] += 1
			elif mem.town_hall == 12:
				bd[1] += 1
			elif mem.town_hall == 11:
				bd[2] += 1
			else:
				bd[3] += 1
			mr = mr +'\n  ' + template.format(str(mem.tag), mem.name, str(mem.town_hall))
		
		em = discord.Embed(title = f"- {clan.name} members list", description = f'```asciidoc\n{mr}\n```', color = 0x1ef686)
		em.add_field(name = "BD", value = "```asciidoc\n[ " + '{0}/{1}/{2}/../{3}'.format(*bd) + ' | ' + str(total) +' total accounts ]\n```')

		await ctx.send(embed = em)

def setup(client):
	client.add_cog(General(client))