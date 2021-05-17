

async def update_totals(member):
    invites = await member.guild.invites()

    c = datetime.today().strftime("%Y-%m-%d").split("-")
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with client.db.execute("SELECT id, uses FROM invites WHERE guild_id = ?", (member.guild.id,)) as cursor: # this gets the old invite counts
        async for invite_id, old_uses in cursor:
            for invite in invites:
                if invite.id == invite_id and invite.uses - old_uses > 0: # the count has been updated, invite is the invite that member joined by
                    if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7): # year can only be less or equal, month can only be less or equal, then check days
                        print(invite.id)
                        await client.db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
                        await client.db.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)", (invite.guild.id, invite.inviter.id, member.id))
                        await client.db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    else:
                        await client.db.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    return
    
# events
@client.event
async def on_member_join(member):
    await update_totals(member)
    await client.db.commit()
        
@client.event
async def on_member_remove(member):
    cur = await client.db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?", (member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        return
    
    inviter = res[0]
    
    await client.db.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
    await client.db.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, memebr.id))
    await client.db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter))
    await client.db.commit()

@client.event
async def on_invite_create(invite):
    await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
    await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
    await client.db.commit()
    
@client.event
async def on_invite_delete(invite):
    await client.db.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
    await client.db.commit()

@client.event
async def on_guild_join(guild): # add new invites to monitor
    for invite in await guild.invites():
        await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses), VAlUES (?,?,?)", (guild.id, invite.id, invite.uses))
        
    await client.db.commit()
    
@client.event
async def on_guild_remove(guild): # remove all instances of the given guild_id
    await client.db.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

    await client.db.commit()
    
# commands
@client.command()
async def invites(ctx, member: discord.Member=None):
    if member is None: member = ctx.author

    # get counts
    cur = await client.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (ctx.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        normal, left, fake = 0, 0, 0

    else:
        normal, left, fake = res

    total = normal - (left + fake)
    
    em = discord.Embed(
        title=f"Invites for {member.name}#{member.discriminator}",
        description=f"{member.mention} currently has **{total}** invites. (**{normal}** normal, **{left}** left, **{fake}** fake).",
        timestamp=datetime.now(),
        colour=discord.Colour.orange())

    await ctx.send(embed=em)
    
async def setup():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("inviteData.db")
    await client.db.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")
    
    # fill invites if not there
    for guild in client.guilds:
        for invite in await guild.invites(): # invites before client was added won't be recorded, invitemanager/tracker don't do this
            await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
            await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (guild.id, invite.inviter.id, 0, 0, 0))
                                 
    await client.db.commit()

client.loop.create_task(setup())
client.run()
asyncio.run(client.db.close())