import json
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

#TODO: ADD PERMISSIONS TO COMMANDS  
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
            name="motivo",
            description="Perchè stai espellendo questo utente?",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ]
)
async def kick(ctx, user, motivo="Nessun motivo fornito."):
    
    # Vars
    guild = await ctx.get_guild()
    ClientKickEmbed = Embeds.KickEmbed
    ServerKickEmbed = Embeds.ServerKickEmbed

    # Embed Settings
    ServerKickEmbed.add_field(name="👨 Utente: ", value=user.name, inline=False)
    ServerKickEmbed.add_field(name="📒 Motivo: ", value=motivo, inline=False)
    ClientKickEmbed.add_field(name="👮 Moderatore: ", value=ctx.author.name, inline=False)
    ClientKickEmbed.add_field(name="📒 Motivo: ", value=motivo, inline=False)

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
            name="motivo",
            description="Perchè stai bandendo questo utente?",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ]
)
async def ban(ctx, user, motivo="Nessun motivo inserito."):
    
    # Vars
    guild = await ctx.get_guild()
    EmbedClient = Embeds.BanEmbed
    Embed = Embeds.ServerBanEmbed

    # Embed Settings
    EmbedClient.add_field("👮 Moderatore: ", value=ctx.author.name)
    EmbedClient.add_field("📒 Motivo: ", value=motivo)
    Embed.add_field("👨 Utente: ", value=user.name, inline=False)
    Embed.add_field("📒 Motivo: ", value=motivo, inline=False)

    # Actions
    await ctx.send(embeds=Embed)
    await user.send(embeds=EmbedClient)
    await user.ban(guild.id, motivo)


Bot.start()