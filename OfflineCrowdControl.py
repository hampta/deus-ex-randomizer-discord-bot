# Can't use real Crowd Control?  Get a taste of the experience with this!

import asyncio
import contextlib
import datetime
import json
import random
import socket
import threading

import discord

from config import (AMMO, AUGS, CHANNEL_ID, COLOR, DESCRIPTION, EFFECTS,
                    EFFECTS_COUNT, EFFECTS_HISTORY, FOOTER, GUILD_ID, HOST,
                    INLINE, PORT, THUMBNAIL, TITLE, TOKEN, VOITING_TIME)

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)


class CrowdControl:
    def __init__(self, host, port):
        self.socket = socket.create_server((host, port))
        self.socket.settimeout(0.1)

    def generate_message(self, code: int, param: str, viewer: str) -> str:
        msg = {
            "id": 1,
            "viewer": viewer,
            "code": code,
            "type": 1,
        }
        if param:
            msg["parameters"] = param
        return json.dumps(msg) + "\0"

    def randomAug(self):
        return random.choice(AUGS).lower()

    def randomAmmo(self):
        return random.choice(AMMO).lower()

    def pickEffect(self):
        return random.choice(EFFECTS)

    def sendEffect(self, effect, viewer):
        msg = self.generate_message(effect[0], effect[1], viewer)
        print(f"Sending {msg}")
        with contextlib.suppress(Exception):
            self.conn.send(msg.encode('utf-8'))

    def __start(self):
        while True:
            with contextlib.suppress(socket.timeout):
                self.conn, addr = self.socket.accept()
                print(f"{addr[0]}:{addr[1]} connected")

    def start(self):
        th = threading.Thread(target=self.__start,
                              daemon=True, name="CrowdControl")
        th.start()


crowd_control = CrowdControl(HOST, PORT)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Guild: {bot.get_guild(GUILD_ID)}")
    print(f"Channel: {bot.get_channel(CHANNEL_ID)}")
    print("------------------")
    print("Starting Crowd Control")
    crowd_control.start()


async def generate_embed():
    random_effects = [crowd_control.pickEffect() for _ in range(EFFECTS_COUNT)]

    embed = discord.Embed(title=TITLE, description=DESCRIPTION, color=COLOR)
    embed.set_thumbnail(url=THUMBNAIL)

    for i, effect in enumerate(random_effects):
        effect_name = effect[0].replace("_", " ").title()
        if effect[1]:
            try:
                effect_name = effect_name.split(
                    " ")[0] + " " + " ".join(effect[1]) + " " + " ".join(effect_name.split(" ")[1:])
            except Exception:
                print(effect_name)
        embed.add_field(name=f"{i+1}. {effect_name}", value="‎", inline=INLINE)
    embed.set_footer(text=FOOTER.format(VOITING_TIME=VOITING_TIME))
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    return embed, random_effects


async def clear_reactions(message, reaction):
    async for user in reaction.users():
        if user != bot.user:
            await message.remove_reaction(reaction.emoji, user)
        await asyncio.sleep(0.1)


async def add_reactions(message, i):
    await message.add_reaction(f"{i}\N{COMBINING ENCLOSING KEYCAP}")
    await asyncio.sleep(0.1)


async def send_message(ctx, embed, current_effects: list, random_effects: list, message, edit):

    results = {}

    reaction: discord.Reaction
    message: discord.Message

    if edit:
        message = await message.edit(embed=embed)
    else:
        message = await ctx.send(embed=embed)

    for i in range(1, EFFECTS_COUNT+1):
        asyncio.create_task(add_reactions(message, i))

    def check(reaction, user):
        if user != bot.user and str(reaction.emoji) in [f"{i}\N{COMBINING ENCLOSING KEYCAP}" for i in range(1, EFFECTS_COUNT+1)]:
            number = reaction.emoji.replace(
                "\N{COMBINING ENCLOSING KEYCAP}", "")
            print(f"{user.name} voted for {number}")
            if results.get(number, ""):
                results[number] = [
                    f"{results[number][0]}, {user.name}", results[number][1] + 1]
            else:
                results[number] = [user.name, 1]
        return False

    with contextlib.suppress(Exception):
        reaction, user = await bot.wait_for("reaction_add", timeout=VOITING_TIME, check=check)

    # fetch the message again to get the latest reactions
    message = await ctx.fetch_message(message.id)
    # fast remove users reactions
    for reaction in message.reactions:
        asyncio.create_task(clear_reactions(message, reaction))

    results = dict(
        sorted(results.items(), key=lambda item: item[1][1], reverse=True))
    try:
        effect = random_effects[int(list(results.keys())[0][0])-1]
        effect_submitter = results[list(results.keys())[0]][0]
    except IndexError:
        effect = random_effects[0]
        effect_submitter = "Nobody"
    crowd_control.sendEffect(effect, effect_submitter)
    if len(current_effects) > EFFECTS_HISTORY:
        current_effects.pop(0)
    current_effects.append(effect)
    effects_history = "\n".join(
        [f"{i+1}. {effect[0].replace('_', ' ').title()}" for i, effect in enumerate(current_effects)])
    await message.edit(f"```Effects history:\n{effects_history}```", embed=embed)
    return message, current_effects


@bot.slash_command(name="start")
async def start(ctx: discord.Interaction):
    if ctx.channel.id != CHANNEL_ID:
        return await ctx.respond("You can't use this command here!")
    await ctx.respond("Done", ephemeral=True)
    current_effects = []
    embed, random_effects = await generate_embed()
    message, current_effects = await send_message(ctx, embed, current_effects, random_effects, edit=False, message=None)

    while True:
        embed, random_effects = await generate_embed()
        message, current_effects = await send_message(ctx, embed, current_effects, random_effects, edit=True, message=message)


bot.run(TOKEN)
