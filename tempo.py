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

TOKEN: str = config.TOKEN
CHANNEL_ID_TEMPO: str = config.CHANNEL_ID_TEMPO  # ID du salon pour la couleur du jour
CHANNEL_ID_LEND: str = config.CHANNEL_ID_LEND  # ID du salon pour la couleur du lendemain

# Mapping des couleurs en français
COULEURS_FRANCAISES = {
    'BLUE': 'BLEU',
    'WHITE': 'BLANC',
    'RED': 'ROUGE',
}

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.command()
async def jour(ctx):
    # Obtenir la date du jour et du lendemain
    current_date = datetime.now().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Formater les dates en français
    formatted_current_date = datetime.strptime(current_date, '%Y-%m-%d').strftime('%d %B %Y')
    formatted_tomorrow_date = datetime.strptime(tomorrow_date, '%Y-%m-%d').strftime('%d %B %Y')

    # Construire l'URL avec les dates dynamiques
    url = f"https://www.myelectricaldata.fr/rte/tempo/{current_date}/{tomorrow_date}"

    # Effectuer la requête HTTP
    response = requests.get(url)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Convertir la réponse JSON en un dictionnaire Python
        data = response.json()

        # Séparer les dates du jour et du lendemain
        current_date_color = data.get(current_date, "N/A")
        tomorrow_date_color = data.get(tomorrow_date, "N/A")

        # Traduire les couleurs en français
        current_date_color_fr = COULEURS_FRANCAISES.get(current_date_color, current_date_color)
        tomorrow_date_color_fr = COULEURS_FRANCAISES.get(tomorrow_date_color, tomorrow_date_color)
        
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

        # Envoyer les informations dans le channel Discord avec les dates formatées
        await ctx.send(f"La couleur du jour *({formatted_current_date})* est : **{current_date_color_fr}**")
        await ctx.send(f"La couleur de demain *({formatted_tomorrow_date})* est : **{tomorrow_date_color_fr}**")
    else:
        await ctx.send(f"La requête a échoué avec le code {response.status_code}.")

# Run the bot
client.run(TOKEN)