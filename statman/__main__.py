import os
import random
import json
import pathlib

import maya
import discord
import callofduty

from callofduty import Mode, Platform, Title

from profile import Profile
from leaderboard import Leaderboard

from commands import command, CommandHandler


client = discord.Client()

cod_username = None
cod_password = None

from usernames import usernames



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type != discord.ChannelType.private:
        if client.user not in message.mentions:
            return

    parts = message.clean_content.split()

    if f"@{client.user.name}" in parts:
        parts.remove(f"@{client.user.name}")

    try:
        requested_command = parts.pop(0)
    except IndexError:
        requested_command = "help"

    actual_command = CommandHandler.registered_commands.get(requested_command)

    if actual_command is None:
        return await message.channel.send(random.choice([
            f"Hmmm... I'm not sure what you mean by '{requested_command}'",
            f"Try again. '{requested_command}' isn't a valid command",
            f"'{requested_command}', more like '{requested_command}', amirite?",
            f"01000111 01000101 01010100 00100000 01010010 01000101 01001011 01010100. '{requested_command}' wasn't in my database.",
            f"{message.author.display_name} used '{requested_command}'. It wasn't very effective.",
        ]))

    try:
        await actual_command(message)
    except Exception as e:
        print(e)
        await message.channel.send("Oooops, something when wrong.")


@command("help")
async def help(message):
    await message.channel.send(f"Here are the commands I have available: {', '.join(f'**{c}**' for c in CommandHandler.registered_commands.keys())}.\nTry _@{client.user.name} <command>_.")


@command("leaderboard")
async def leaderboard(message):
    cod = await callofduty.Login(cod_username, cod_password)

    profiles = [
        Profile(await (await cod.GetPlayer(*username["cod_username"])).profile(Title.ModernWarfare, Mode.Warzone))
        for username in usernames
    ]

    await message.channel.send(Leaderboard(profiles).as_message())


@command("statme")
async def statme(message):
    cod = await callofduty.Login(cod_username, cod_password)

    username = next((user for user in usernames if user["discord_id"] == message.author.id), None)

    if not username:
        return await message.channel.send("I'm sorry, I don't have you registed yet. Ask @fatman to get his shit together.")

    profile = Profile(await (await cod.GetPlayer(*username["cod_username"])).profile(Title.ModernWarfare, Mode.Warzone))

    json.dump(profile.data, open("stats.json", "w"))

    response = [
        f"{message.author.display_name}, here's your stats so far this week in Warzone:\n",
        f":video_game:  Games played: **{profile.games_played:,.0f}**",
        f":skull_crossbones:  KD: **{profile.kd:,.2f}**",
        f":skull:  Kills: **{profile.kills:,.0f}**",
        f":muscle:  Assists: **{profile.assists:,.0f}**",
        f":ambulance:  Revives: **{profile.revives:,.0f}**",
        f":boom:  Damage done: **{profile.damage_done:,.0f}**",
        f":exploding_head:  Headshots: **{profile.headshots:,.0f}**",
        f":package:  Caches opened: **{profile.caches_opened:,.0f}**",
    ]

    return await message.channel.send("\n".join(response))


@command("lastgame")
async def lastgame(message):
    cod = await callofduty.Login(cod_username, cod_password)

    username = next((user for user in usernames if user["discord_id"] == message.author.id), None)

    last_match = (await cod.GetPlayerMatches(username["cod_username"][0], username["cod_username"][1], Title.ModernWarfare, Mode.Warzone))[0]

    full_details = await cod.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, last_match.id)

    this_player = next((player for player in full_details["allPlayers"] if player["player"]["username"] == username["cod_username"][1].split("#")[0]), None)

    team = [
        player for player in full_details["allPlayers"]
        if player["player"]["team"] == this_player["player"]["team"]
    ]

    match_start = maya.MayaDT(team[0]["utcStartSeconds"])

    return await message.channel.send(f"Your last game started {match_start.slang_time()} at {match_start.rfc2822()}. You got {this_player['playerStats']['kills']:.0f} kills.")


@command("dropin")
async def dropin(message):
    location = random.choice([
        "Quarry"
        "Airport",
        "Hangers",
        "Storage Town",
        "Hospital",
        "Train Station",
        "Promenade East",
        "Promenade west",
        "TV Station",
        "Stadium",
        "Lumber Yard",
        "Prison",
        "Port",
        "Superstore",
        "Farmland",
        "Park",
        "Hills",
        "Boneyard",
        "Military Base",
        "Dam",
    ])

    return await message.channel.send(random.choice([
        f"I think you'll have the most luck at **{location}**.",
        f"Go **{location}**, you won't.",
        f"Your LZ is **{location}**.",
        f"All the best loot is going to be at **{location}**, trust me I'm a bot.",
        f"**{location}** - GO GO GO!",
        f"Easy claps at **{location}**.",
        f"Grab the closest bounty to **{location}**.",
        f"Go **{location}** or home.",
    ]))



if __name__ == "__main__":
    with open(pathlib.Path(os.path.dirname(os.path.realpath(__file__)), "details.json"), "r") as f:
        details = json.load(f)
    cod_username = details["cod_username"]
    cod_password = details["cod_password"]
    client.run(details["discord_token"])
