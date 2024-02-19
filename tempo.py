from re import A
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import locale
import config  # Importez les variables depuis config.py

# Définir la locale en français
locale.setlocale(locale.LC_ALL, "")

# Définir les intentions nécessaires
intents = discord.Intents.default()
intents.message_content = True  # Pour les événements de messages

# GERER LES VARIABLES DU CONFIG.PY
TOKEN: str = config.TOKEN
CHANNEL_ID_TEMPO: str = config.CHANNEL_ID_TEMPO
CHANNEL_ID_LEND: str = config.CHANNEL_ID_LEND
CHANNEL_ID_ENVOI: str = config.CHANNEL_ID_ENVOI
HEURE_LANCEMENT: str = config.HEURE_LANCEMENT

# Mapping des couleurs en français
COULEURS_FRANCAISES = {
    'BLUE': 'BLEU',
    'WHITE': 'BLANC',
    'RED': 'ROUGE',
}

client = commands.Bot(command_prefix='!', intents=intents)

# Bon, ça, c'est pour mettre les couleurs dans l'embed du texte du channel
def map_color_to_discord_color(color_text):
    color_text_lower = color_text.lower()  # Convertir en minuscules pour une correspondance insensible à la casse
    color_mapping = {
        'blue': discord.Colour.from_rgb(0, 0, 255),
        'white': discord.Colour.from_rgb(255, 255, 255),
        'red': discord.Colour.from_rgb(255, 0, 0),
        # Ajoutez d'autres couleurs au besoin
    }

    return color_mapping.get(color_text_lower, discord.Color.default())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.command()
async def tempo(ctx):
    await ctx.message.delete() # suprime l'appel
    # Obtenir la date du jour et du lendemain
    current_date = datetime.now().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Formater les dates en français
    formatted_current_date = datetime.strptime(current_date, '%Y-%m-%d').strftime('%d %B %Y')
    formatted_tomorrow_date = datetime.strptime(tomorrow_date, '%Y-%m-%d').strftime('%d %B %Y')

    # On prend le swagger du poto MED :) 
    url = f"https://www.myelectricaldata.fr/rte/tempo/{current_date}/{tomorrow_date}"
    url2 = f"https://www.myelectricaldata.fr/edf/tempo/days"

    # Effectuer la requête HTTP
    response = requests.get(url)
    response2 = requests.get(url2)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Convertir la réponse JSON en un dictionnaire Python
        data = response.json()
        data2 = response2.json()

        # Séparer les dates du jour et du lendemain
        current_date_color = data.get(current_date, "NON DISPONIBLE ACTUELLEMENT")
        tomorrow_date_color = data.get(tomorrow_date, "NON DISPONIBLE ACTUELLEMENT")
        rouge_restant = data2.get("red", "N/A")
        blanc_restant = data2.get("white", "N/A")
        bleu_restant = data2.get("blue", "N/A")

        # Traduire les couleurs en français
        current_date_color_fr = COULEURS_FRANCAISES.get(current_date_color, current_date_color)
        tomorrow_date_color_fr = COULEURS_FRANCAISES.get(tomorrow_date_color, tomorrow_date_color)
        
        # Récupérer les couleurs Discord associées
        current_day_discord_color = map_color_to_discord_color(current_date_color)
        tomorrow_discord_color = map_color_to_discord_color(tomorrow_date_color)
        
        # Afficher la couleur du jour dans le salon correspondant
        channel_day = client.get_channel(int(CHANNEL_ID_TEMPO))
        new_channel_name_day = f"Aujourd'hui - {current_date_color_fr}"

        if channel_day:
            await channel_day.edit(name=new_channel_name_day)
        else:
            await ctx.send("Impossible de trouver le salon pour la couleur du jour avec l'ID spécifié.")

        # Afficher la couleur du lendemain dans le salon corresponda
        channel_tomorrow = client.get_channel(int(CHANNEL_ID_LEND))
        new_channel_name_tomorrow = f"Demain - {tomorrow_date_color_fr}"

        if channel_tomorrow:
                await channel_tomorrow.edit(name=new_channel_name_tomorrow)
        else:
                await ctx.send("Impossible de trouver le salon pour la couleur du lendemain avec l'ID spécifié.")
                
        # Envoyer les informations dans le channel Discord avec les dates formatées en utilisant un embed
        channel_id_to_send = (int(CHANNEL_ID_ENVOI))
        if ctx.guild:  # Vérifie si la commande est exécutée dans un serveur
            channel_to_send = ctx.guild.get_channel(int(channel_id_to_send))
        
        if channel_to_send:
            # Créer un embed pour la couleur du jour
            embed = discord.Embed(color=current_day_discord_color)
            embed.add_field(name=f"Couleur du jour ({formatted_current_date})", value=f"**{current_date_color_fr}**")

            # Créer un embed pour la couleur du lendemain
            embed_tomorrow = discord.Embed(color=tomorrow_discord_color)
            embed_tomorrow.add_field(name=f"Couleur de demain ({formatted_tomorrow_date})", value=f"**{tomorrow_date_color_fr}**")

            # Envoyer les embeds uniquement dans le channel spécifié
            await channel_to_send.send(embed=embed)
            await channel_to_send.send(embed=embed_tomorrow)
            await channel_to_send.send(f".\n **:blue_circle: :** {bleu_restant} jours restants\n **:white_circle: :** {blanc_restant} jours restants\n **:red_circle: :** {rouge_restant} jours restants jusqu'au 31 mars")
        else:
            await ctx.send("Impossible de trouver le channel avec l'ID spécifié.")
    else:
        await ctx.send("Cette commande ne peut être exécutée que dans un serveur.")

# Run the bot
client.run(TOKEN)
