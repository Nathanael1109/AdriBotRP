from discord.ext import commands
import os
import discord
import keep_on
import random
import time
import json
import asyncio

        
keep_on.keep_on()
bot = commands.Bot(command_prefix='!', description="Un bot pour le serveur de jeux de rôle d'Adrien", owner_id=276984195342139392, case_insensitive=True, pm_help=True, help_command=None)

owner_id = 276984195342139392

format_debug = time.strftime("######## LOGS - DEBUG %d/%m/%Y %H:%M:%S ######## ")
format_error = time.strftime("######## /!\ LOGS - ERROR /!\ %d/%m/%Y %H:%M:%S ######## ")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.playing,
                                  name="!help"))
    
    print(" ")
    print(format_debug)
    print("BOT STARTED")
    print(format_debug)
    print(" ")


@bot.command()
async def temp1(ctx):
    await ctx.send("message 1")
    await ctx.send("message 2")
    await ctx.send("message 3")
    await ctx.send("message 4")
    await ctx.send("message 5")
    await ctx.send("message 6")
    await ctx.send("message 7")
    await ctx.send("message 8")
    await ctx.send("message 9")
    await ctx.send("message 10")
    await ctx.send("message 11")
    await ctx.send("message 12")
    await ctx.send("message 13")
    await ctx.send("message 14")
    await ctx.send("message 15")


@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    
    message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
    await ctx.reply(message)



@bot.command()
async def clear(ctx, amount=1):
    if amount >= 21:
        await ctx.send("Vous ne pouvez pas supprimer plus de 20 messages en une fois.")
    else:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} messages supprimés")
        messages = await ctx.channel.history(limit=1).flatten()
        await asyncio.sleep(5)
        for message in messages:
            await message.delete()

@bot.command()
async def clearforce(ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} messages supprimés")
        messages = await ctx.channel.history(limit=1).flatten()
        await asyncio.sleep(5)
        for message in messages:
            await message.delete()


@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong ! {round(bot.latency * 1000)}ms")


@bot.command()
async def roll(ctx):
    nombre = int(ctx.message.content.split(" ")[1])
    total = int(0)
    if nombre > 10:
        await ctx.reply("Vous ne pouvez pas faire plus de 10 lancés")
    else:
        while nombre > 0:
            gen = random.randint(1, int(ctx.message.content.split(" ")[2]))
            await ctx.send("Roll: {}".format(gen))
            total = total + gen
            nombre -= 1
        total = str(total)
        await ctx.reply("total: " + total)


@bot.command()
async def register(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)

    if not ctx.author.discriminator in data:
        data[ctx.author.discriminator] = {}
        data[ctx.author.discriminator]["name"] = ctx.message.content.split(" ")[1]
        data[ctx.author.discriminator]["pv"] = 20
        data[ctx.author.discriminator]["xp"] = 0
        data[ctx.author.discriminator]["level"] = 1
        data[ctx.author.discriminator]["money"] = 0
        data[ctx.author.discriminator]["force"] = 0
        data[ctx.author.discriminator]["dexterite"] = 0
        data[ctx.author.discriminator]["intelligence"] = 0
        data[ctx.author.discriminator]["sagesse"] = 0
        data[ctx.author.discriminator]["constitution"] = 0
        data[ctx.author.discriminator]["charisme"] = 0
        with open('./users.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.reply("Vous êtes inscrit")
    else:
        await ctx.reply("Vous êtes déjà inscrit")


@bot.command()
async def unregister(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)

    if ctx.author.discriminator in data:
        with open('./users.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.reply("***VOUS ALLEZ ETRE DESINSCRIT AUCUN RETOUR EN ARRIERE POSSIBLE*** \n(pour confirmer, réagissez avec ✅ sur votre message de commande) \n(pour annuler, réagissez avec ❌ sur votre message de commande)")
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == ctx.message.id and str(reaction.emoji) in ['✅', '❌']
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("Vous avez dépassé le temps d'attente")
        else:
            if str(reaction.emoji) == '✅':
                del data[ctx.author.discriminator]
                with open('./users.json', 'w') as f:
                    json.dump(data, f, indent=4)
                await ctx.reply("Vous êtes désinscrit")
            else:
                await ctx.reply("Vous avez annulé")
    else:
        await ctx.reply("Vous n'êtes pas inscrit")

@bot.command()
async def levelup(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)

    if ctx.author.discriminator in data:
        if data[ctx.author.discriminator]["xp"] >= 300*data[ctx.author.discriminator]["level"]:
            data[ctx.author.discriminator]["xp"] = data[ctx.author.discriminator]["xp"] - 300*data[ctx.author.discriminator]["level"]
            data[ctx.author.discriminator]["level"] = data[ctx.author.discriminator]["level"] + 1
            with open('./users.json', 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.reply(f"<@{ctx.author.id}> a levelup")
        else:
            await ctx.reply("vous n'avez pas assez d'xp")
    else:
        await ctx.reply("Vous n'êtes pas inscrit")


@bot.command()
async def stats(ctx, tag=None):
    if tag == None:
        tag = ctx.author.discriminator

    with open('./users.json', 'r') as f:
        data = json.load(f)

    if tag in data:
        await ctx.reply(f"```Profil de {tag} :```\n"
                        f"Nom: `{data[tag]['name']}`\n"
                        "\n"
                        f"Niveau: `{data[tag]['level']}`\n"
                        f"XP: `{data[tag]['xp']}`\n"
                        "\n"
                        f"Argent: `{data[tag]['money']}`\n"
                        "\n"
                        f"Force: `{data[tag]['force']}`\n"
                        f"Dexterité: `{data[tag]['dexterite']}`\n"
                        f"Intelligence: `{data[tag]['intelligence']}`\n"
                        f"Sagesse: `{data[tag]['sagesse']}`\n"
                        f"Constitution: `{data[tag]['constitution']}`\n"
                        f"Charisme: `{data[tag]['charisme']}`\n"
                        f"PV: `{data[tag]['pv']}`\n"
                        "\n"
                        f"Pour tout probléme, contactez <@{owner_id}>"
                        "\n"
                        )

    else:
        await ctx.reply("Vous n'êtes pas inscrit")
        

@bot.command()
async def stat(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)
    stat = str(ctx.message.content.split(" ")[2])
    tag = str(ctx.message.content.split(" ")[1])
    
    if tag in data:
        if stat in data[tag]:
           await ctx.reply(f"```Statistique spécifique de {tag} :```\n"
                        f"{stat}: `{data[tag][stat]}`\n"
                        )
        else: 
            await ctx.reply("Vous n'avez pas cette statistique")
    else:
        await ctx.reply("Vous n'êtes pas inscrit")


@bot.command()
async def md_stat(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)
    tag = str(ctx.message.content.split(" ")[1])
    stat = str(ctx.message.content.split(" ")[2])
    set_ammount = str(ctx.message.content.split(" ")[3])
    if tag in data:
        if stat == "name":
            await ctx.reply("Vous ne pouvez pas changer le nom d'un joueur, cela causerais des probléme, pour modifier le nom, contactez Nathanaël#0406")
        elif stat == "name_force":
            old_value = data[tag]["name"]
            stat = "name"
            data[tag][stat] = (set_ammount)
            with open('./users.json', 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.reply(f"```Modification FORCE de la statistique de {tag} :```\n"
                        f"{stat}: `{old_value}` -> `{data[tag][stat]}`\n"
                        f"ATTENTION CECI PEUT CUASER DES CORRUPTION DE PROFILS, SI C'EST LE CAS, CONTACTEZ NATHANAEL#0406 \n"
                        )
        elif stat in data[tag]:
            old_value = data[tag][stat]
            data[tag][stat] = int(set_ammount)
            with open('./users.json', 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.reply(f"```Modification de la statistique de {tag} :```\n"
                        f"{stat}: `{old_value}` -> `{data[tag][stat]}`\n"
                        )
        
        else: 
            await ctx.reply("le joueur n'a pas cette statistique")

    else:
        await ctx.reply("le joueur n'êtes pas inscrit")

@bot.command()
async def pv(ctx):
    with open('./users.json', 'r') as f:
        data = json.load(f)
    tag = str(ctx.message.content.split(" ")[1])
    if tag in data:
        await ctx.reply(f"```PV de {tag} :```\n"
                        f"PV: `{data[tag]['pv']}`\n"
                        )
    else:
        await ctx.reply("Joueur non-inscrit")

@bot.command()
async def help(ctx):
    await ctx.send("```\n"
                    "!help - Affiche les commandes\n"
                    "!ping - Affiche le ping du bot\n"
                    "!clear [Combres de messages]- Supprime les messages\n"
                    "!register [Nom] - Inscrit un utilisateur\n"
                    "!unregister - Désinscrit un utilisateur\n"
                    "!levelup - Augmente le niveau d'un utilisateur\n"
                    "!stats [TagDiscord] - Affiche les stats d'un utilisateur\n"
                    "!stat [TagDiscord] [Stat] - Affiche les stats spécifiques d'un utilisateur\n"
                    "!md_stat [TagDiscord] [Stat] [NV_Valeure] - Modifie les stats d'un utilisateur\n"
                    "\n"
                    f"Pour tout probléme, contactez <@{owner_id}>"
                    "\n"
                     "```")


token = os.environ['TOKEN']
bot.run(token)

# f"<@{ctx.author.id}>" fonctionne pour récupérer ping l'id
# "\n"
# f"Pour tout probléme, contactez <@{owner_id}>"
# "\n"

    

