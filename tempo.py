import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

# Définir les intentions nécessaires
intents = discord.Intents.default()
intents.message_content = True  # Pour les événements de messages

TOKEN = ''
CHANNEL_ID = '1206593461382553633'

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.command()
async def get_tempo_color(ctx):
    url = 'https://www.services-rte.com/fr/visualisez-les-donnees-publiees-par-rte/calendrier-des-offres-de-fourniture-de-type-tempo.html'
    

    # Récupérer la page HTML
    response = requests.get(url)
    
    # Vérifier si la requéte a réussi (code 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser la page HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        BeautifulSoup.BeautifulSoup(url.decode('utf-8','ignore'))
        
        # Supposons que la couleur du jour est dans une balise avec la classe "current-day"
        current_day_color_element = soup.find('div', class_='c-tempo__bloc-1__body')

        # Extraire la couleur du jour
        if current_day_color_element:
            current_day_color = current_day_color_element.text.strip()
            await ctx.send(f"La couleur Tempo du jour est : {current_day_color}")
        else:
            await ctx.send("Impossible de trouver la couleur du jour Tempo.")
    else:
        await ctx.send(f"La requete a échoué avec le code {response.status_code}.")

@client.command()
async def jour(ctx):
    await get_tempo_color(ctx)  # Appeler la fonction existante pour obtenir la couleur du jour

# Run the bot
client.run(TOKEN)
