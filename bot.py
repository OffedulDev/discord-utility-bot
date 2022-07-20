from copy import copy
from distutils.command.build import build
from email.policy import default
import json
from pydoc import describe
from unittest import addModuleCleanup
from xmlrpc.client import Server
from click import option
import interactions
class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

Bot = interactions.Client(token="OTk3MTMyMTI0MDQ4MDY4Nzg4.GzHUcy.UHUZs4_5B8plaalx8j9Cp1t9ehwlSLWneOVz6U")

    
class Embeds:
    BanEmbed = interactions.Embed(title="🛑 Sei stato bannato. 🛑", description="Sei stato bandito da Diamond City, seguano i dettagi del tuo ban.", color=colors.red)
    ServerBanEmbed = interactions.Embed(title="✅ Utente Bannato", description="Hai bannato l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    KickEmbed = interactions.Embed(title="⚠️ Sei stato Espulso. ⚠️", description="Sei stato espulso da Diamond City, seguano i dettagi del tuo ban.", color=colors.red)
    ServerKickEmbed = interactions.Embed(title="✅ Utente Espulso", description="Hai espulso l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    WarnEmbed = interactions.Embed(title="🪖 Sei stato avvertito! 🪖", description="Sei stato avvertito, seguano i dettagli del tuo avvertimento.", color=colors.orange)
    ServerWarnEmbed = interactions.Embed(title="✅ Utente Avvertito", description="Hai avvertito l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)

# JSON Functions
async def build_user_data(user_id):

    user_data = {
        "warn_amount": "0"
    }
    
    return user_data

async def read_json_value(value):
    with open('data.json', "r+") as file:
        Data = json.loads(file.read())
        Data = Data["data"]
        file.close()
        return Data[value]
        
async def write_json_value(key, data):
    with open('data.json', "r+") as file:
        Data = json.loads(file.read())
        Data["data"][key] = data

        file.seek(0)
        json.dump(Data, file, indent=4)  
        file.close()  

# Kick Command
@Bot.command(
    name="kick",
    description="Espelli un utente dal server.",
    options=[
        interactions.Option(
            name="user",
            description="La tag dell'utente che vorresti espellere.",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="reason",
            description="Perchè stai espellendo questo utente?",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ],
    default_member_permissions=interactions.Permissions.KICK_MEMBERS
)
async def kick(ctx, user, reason="Nessun reason fornito."):
    
    # Vars
    guild = await ctx.get_guild()
    
    ClientKickEmbed = copy(Embeds.KickEmbed)
    ServerKickEmbed = copy(Embeds.ServerKickEmbed)

    # Embed Settings
    ServerKickEmbed.add_field(name="👨 Utente: ", value=user.name, inline=False)
    ServerKickEmbed.add_field(name="📒 Motivo: ", value=reason, inline=False)
    ClientKickEmbed.add_field(name="👮 Moderatore: ", value=ctx.author.name, inline=False)
    ClientKickEmbed.add_field(name="📒 Motivo: ", value=reason, inline=False)

    # Actions
    await user.send(embeds=ClientKickEmbed)
    await ctx.send(embeds=ServerKickEmbed, ephemeral=True)
    await user.kick(guild.id, reason)

# Ban Command
@Bot.command(
    name="ban",
    description="Bandisci un utente dal server in questione.",
    options=[
        interactions.Option(
            name="user",
            description="La tag dell'utente che vorresti bandire.",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="reason",
            description="Perchè stai bandendo questo utente?",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ],
    default_member_permissions=interactions.Permissions.BAN_MEMBERS
)
async def ban(ctx, user, reason="Nessun reason inserito."):
    
    # Vars
    guild = await ctx.get_guild()
    EmbedClient = copy(Embeds.BanEmbed)
    Embed = copy(Embeds.ServerBanEmbed)

    # Embed Settings
    EmbedClient.add_field("👮 Moderatore: ", value=ctx.author.name)
    EmbedClient.add_field("📒 Motivo: ", value=reason)
    Embed.add_field("👨 Utente: ", value=user.name, inline=False)
    Embed.add_field("📒 Motivo: ", value=reason, inline=False)

    # Actions
    await ctx.send(embeds=Embed)
    await user.send(embeds=EmbedClient, ephemeral=True)
    await user.ban(guild.id, reason)

# Warn Command
@Bot.command(
    name="warn",
    description="Avverti un utente.",
    options=[
        interactions.Option(
            name="user",
            description="Utente da avvertire.",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="reason",
            description="Motivo dell'avvertimento.",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
    default_member_permissions=interactions.Permissions.KICK_MEMBERS
)
async def warn(ctx, user, reason):
    
    # Vars
    UserData = await read_json_value(str(int(user.id)))
    warn_amount = 0

    # Embed Settings
    WarnEmbed = copy(Embeds.WarnEmbed)
    ServerWarnEmbed = copy(Embeds.ServerWarnEmbed)
    WarnEmbed.add_field(name="👮 Moderatore: ", value=ctx.author.name, inline=False)
    WarnEmbed.add_field(name="📒 Motivo: ", value=reason, inline=False)
    ServerWarnEmbed.add_field(name="👨 Utente: ", value=user.name, inline=False)
    ServerWarnEmbed.add_field(name="📒 Motivo: ", value=reason, inline=False)

    # Actions
    if UserData is None:
        # Create and set data.
        UserData = await build_user_data(str(int(user.id)))
        UserData["warn_amount"] = "1"
        warn_amount = UserData["warn_amount"]
        await write_json_value(int(user.id), UserData)
    else:
        # Set data.
        UserData["warn_amount"] = str(int(UserData["warn_amount"]) + 1)
        warn_amount = UserData["warn_amount"]
        await write_json_value(int(user.id), UserData)

    # Set embed and send message.
    ServerWarnEmbed.add_field(name="🛑 Numero di Warn Totali: ", value=str(warn_amount), inline=False)
    WarnEmbed.add_field(name="🛑 Numero di Warn Totali: ", value=str(warn_amount), inline=False)
    await user.send(embeds=WarnEmbed)
    await ctx.send(embeds=ServerWarnEmbed, ephemeral=True)
        

Bot.start()