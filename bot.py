from copy import copy
import datetime
import json
import interactions
import requests
from Bot_TokenFile import token
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

Bot = interactions.Client(token=token)

# Embed Utility
class Embeds:
    BanEmbed = interactions.Embed(title="🛑 Sei stato bannato. 🛑", description="Sei stato bandito da Diamond City, seguano i dettagi del tuo ban.", color=colors.red)
    ServerBanEmbed = interactions.Embed(title="✅ Utente Bannato", description="Hai bannato l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    KickEmbed = interactions.Embed(title="⚠️ Sei stato Espulso. ⚠️", description="Sei stato espulso da Diamond City, seguano i dettagi del tuo ban.", color=colors.red)
    ServerKickEmbed = interactions.Embed(title="✅ Utente Espulso", description="Hai espulso l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    WarnEmbed = interactions.Embed(title="🪖 Sei stato avvertito! 🪖", description="Sei stato avvertito, seguano i dettagli del tuo avvertimento.", color=colors.orange)
    ServerWarnEmbed = interactions.Embed(title="✅ Utente Avvertito", description="Hai avvertito l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    BadRequest = interactions.Embed(title="🔐 Bad Request", description="La request inviata è stata rifiutata da Discord oppure i parametri sono invalidi.", color=colors.red)
    TimeoutEmbed = interactions.Embed(title="🤐 Sei stato messo in Timeout 🤐", description="Sei stato messo in timeout da un moderatore, durante questo periodo non puoi parlare o entrare nei canali vocali, seguano i dettagli.", color=colors.red)
    ServerTimeoutEmbed = interactions.Embed(title="✅ Utente messo in Timeout", description="Hai messo in timeout l'utente con successo, seguano i dettagli dell'azione.", color=colors.green)
    ModificaApportata = interactions.Embed(title="✅ Modificato con Successo!", description="Seguano i dettagli della modifica che hai apportato.", color=colors.green)
    TicketEmbed = interactions.Embed(title="🔧 Ticket 🗝️", description="Seleziona un opzione qui sotto per aprire un ticket nella rispettiva categoria, segue un messaggio personalizzato.", color=colors.teal)
    OpenTicketEmbed = interactions.Embed(title="👮 Ticket Aperto con Successo 🎭", description="Il tuo ticket è stato aperto e posizionato nella categoria da te richiesta. A breve un membro dello staff sarà da te per assisterti e risolvere o chiarire i tuoi dubbi.", color=colors.green)

# Functions Utility

async def get_channel(id: int):
        try:
            return interactions.Channel(**await Bot._http.get_channel(id), _client=Bot._http)
        except:
            print("Error getting channel")
            return None


# Modal Utility
Modals = {
    "nuova_categoria": [
        interactions.TextInput(
            label="Nome della categoria da aggiungere.",
            style=interactions.TextStyleType.SHORT,
            custom_id="categoryName",
            min_length=1,
            max_length=80
        )
    ],
    "channel": [
        interactions.TextInput(
            label="ID del canale per il messaggio.",
            style=interactions.TextStyleType.SHORT,
            custom_id="channelID",
            min_length=1,
            max_length=19
        )
    ],
    "message": [
        interactions.TextInput(
            label="Messaggio personalizzato.",
            style=interactions.TextStyleType.SHORT,
            custom_id="messageContent",
            min_length=1,
            max_length=19
        )
    ]
}

# HTTP Functions
Base = "https://discord.com/api/v9/"
Default_Headers = {"Authorization": f"Bot {token}"}
async def prepare_api_request(endpoint):
    Request_Url = Base + endpoint
    return Request_Url

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
        try:
            return Data[value]
        except KeyError:
            return None
        
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
        
# Timeout Command
@Bot.command(
    name="timeout",
    description="Metti un utente in timeout.",
    options=[
        interactions.Option(
            name="user",
            description="L'utente da mettere in timeout.",
            type=interactions.OptionType.USER,
            required=True
        ),
        interactions.Option(
            name="time",
            description="Tempo in minuti della durata del timeout.",
            type=interactions.OptionType.INTEGER,
            required=True
        ),
        interactions.Option(
            name="reason",
            description="Motivo dell'timeout.",
            type=interactions.OptionType.STRING,
            required=False
        )
    ],
    default_member_permissions=interactions.Permissions.KICK_MEMBERS
)
async def timeout(ctx, user, time, reason="Nessun motivo inserito."):

    # Vars
    Guild = await ctx.get_guild()
    GuildID = int(Guild.id)
    Endpoint = f"guilds/{GuildID}/members/{int(user.id)}"
    Url = await prepare_api_request(Endpoint)
    time =  (datetime.datetime.utcnow() + datetime.timedelta(minutes=time)).isoformat()
    Json = {'communication_disabled_until': time}

    # Embed Settings
    TimeoutEmbed = copy(Embeds.TimeoutEmbed)
    ServerTimeoutEmbed = copy(Embeds.ServerTimeoutEmbed)
    BadRequestEmbed = copy(Embeds.BadRequest)
    TimeoutEmbed.add_field("👮 Moderatore:", value=ctx.author.name, inline=True)
    TimeoutEmbed.add_field("📒 Motivo:", value=reason, inline=False)
    ServerTimeoutEmbed.add_field("👨 Utente:", value=user.name, inline=True)
    ServerTimeoutEmbed.add_field("📒 Motivo:", value=reason, inline=False)

    # Actions
    Session = requests.patch(Url, json=Json, headers=Default_Headers)
    if Session.status_code in range(200, 299):
        await user.send(embeds=TimeoutEmbed)
        await ctx.send(embeds=ServerTimeoutEmbed, ephemeral=True)
    else:
        BadRequestEmbed.add_field("⚠️ Codice Risposta: ", value=str(Session.status_code), inline=False)
        await ctx.send(embeds=BadRequestEmbed, ephemeral=True)

# Ticket System
# Modals
@Bot.modal("nuova_categoria")
async def nuova_categoria(ctx, category_name):
    
    # Vars
    categories = await read_json_value("categories")
    embed = copy(Embeds.ModificaApportata)

    # Embed Settings
    embed.add_field("📒 Modifica: ", value="Nuova Categoria!", inline=False)

    # Actions
    categories.append(category_name)
    await ctx.send(embeds=embed, ephemeral=True)
    await write_json_value("categories", categories)

@Bot.modal("channel")
async def set_channel(ctx, channelID):
    
    BadRequest = copy(Embeds.BadRequest)
    CompletedEdit = copy(Embeds.ModificaApportata)

    try:
        int(channelID)
    except ValueError:
        BadRequest.add_field("📒 Motivo: ", value="Inserisci un numero di 18 cifre!", inline=False)
        
        await ctx.send(embeds=BadRequest, ephemeral=True)
        return

    ChannelID = int(channelID)
    Channel = await get_channel(ChannelID)
    if Channel is None:
        BadRequest.add_field("📒 Motivo: ", value="Il canale non esiste!", inline=False)
        
        await ctx.send(embeds=BadRequest, ephemeral=True)
        return

    CompletedEdit.add_field("📒 Modifica: ", value="Canale di invio impostato. (" + Channel.name + ")", inline=False)
    
    await write_json_value("channelId", str(int(Channel.id)))
    await ctx.send(embeds=CompletedEdit, ephemeral=True)


@Bot.modal("message")
async def set_message(ctx, messageContent):

    CompletedEdit = copy(Embeds.ModificaApportata)
    CompletedEdit.add_field("📒 Modifica: ", value="Messaggio di invio impostato. (" + messageContent + ")", inline=False)
    
    await write_json_value("messageContent", str(messageContent))
    await ctx.send(embeds=CompletedEdit, ephemeral=True)

# Ticket Setup Command
@Bot.command(
    name="ticket",
    description="Imposta i vari parametri dei ticket.",
    options=[
        interactions.Option(
            name="index",
            description="Cosa vuoi editare?",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    default_member_permissions=interactions.Permissions.ADMINISTRATOR
)
async def ticket_setup(ctx, index):
    
    # Vars
    BadRequestEmbed = copy(Embeds.BadRequest)

    # Embed Settings
    BadRequestEmbed.add_field(name="🛑 Motivo:", value="Nessuna impostazione trovata con la tua index.", inline=False)

    # Actions
    if index in Modals:
        Modal = interactions.Modal(
            title=f"Edit '{index}'",
            custom_id=index,
            components=Modals[index]
        )

        await ctx.popup(Modal)
    else:
        await ctx.send(embeds=BadRequestEmbed, ephemeral=True)

@Bot.component("ticketComponent")
async def openTicket(ctx, category):

    category = category[0]

    # Vars
    Guild = await ctx.get_guild()
    TicketOpened = copy(Embeds.OpenTicketEmbed)
    CloseButton = interactions.Button(
        style=interactions.ButtonStyle.DANGER,
        label="⚠️ Chiudi il Ticket",
        custom_id=ctx.author.name
    )

    # Embed Settings
    TicketOpened.add_field(name="📒 Categoria: ", value=category, inline=False)

    # Actions
    Channel = await Guild.create_channel(name=f"{category.lower()}-{ctx.author.name.lower()}", type=interactions.ChannelType.GUILD_TEXT, topic=f"Ticket creato da {ctx.author.name} in {category}")
    @Bot.component(ctx.author.name)
    async def close(context):
        await Channel.delete()

    await Channel.send(ctx.author.mention)
    await Channel.send(embeds=TicketOpened, components=CloseButton)



@Bot.command(
    name="inviamessaggioticket",
    description="Invia il messaggio per permettere agli utenti di aprire un ticket.",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR
)
async def inviaMessaggioTicket(ctx):
    
    # Vars
    BadRequestEmbed = copy(Embeds.BadRequest)
    TicketEmbed = copy(Embeds.TicketEmbed)

    # Actions
    Options = await read_json_value("categories")
    MessageContent = await read_json_value("messageContent")
    ChannelID = await read_json_value("channelId")
    if (Options == "" or None) or (MessageContent == "" or None) or (ChannelID == "" or None):
        BadRequestEmbed.add_field("📒 Motivo: ", value="Errore data interno o i parametri non sono stati impostati", inline=False)

        await ctx.send(embeds=BadRequestEmbed, ephemeral=True)
        return

    _Options = []
    for Option in Options:
        _Options.append(interactions.SelectOption(
                label=Option,
                value=Option,
                description="Apri un ticket in questa categoria."
            )
        )
    
    Menu = interactions.SelectMenu(
        options=_Options,
        placeholder="Seleziona una categoria per cominciare.",
        custom_id="ticketComponent"
    )

    TicketEmbed.add_field(name="🎭 Messaggio Personalizzato: ", value=MessageContent, inline=False)
    
    Channel = await get_channel(int(ChannelID))

    await Channel.send(embeds=TicketEmbed, components=Menu)
    await ctx.send("Punto di apertura ticket inviato con successo.")
    return

Bot.start()