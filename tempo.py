import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime

# Définir les intentions nécessaires
intents = discord.Intents.default()
intents.message_content = True  # Pour les événements de messages

TOKEN = 'MTIwMzgzMjIyODY1Mjc4MTU4OA.G3MJJ8.oizuGS2jpZt4PtgIVCfj_OT7WGoGOeSWfPK7NA'
CHANNEL_ID_TEMPO = '1206593461382553633'  # ID du salon pour la couleur du jour
CHANNEL_ID_LEND = '1206870641316339712'  # ID du salon pour la couleur du lendemain

client = commands.Bot(command_prefix='!', intents=intents)

# Ajoutez une fonction de mappage des couleurs Discord en fonction du texte
def map_color_to_discord_color(color_text):
    color_text_lower = color_text.lower()  # Convertir en minuscules pour une correspondance insensible à la casse
    color_mapping = {
        'blanc': discord.Colour.from_rgb(255, 255, 255),
        'bleu': discord.Colour.from_rgb(0, 0, 255),
        'rouge': discord.Colour.from_rgb(255, 0, 0),
        # Ajoutez d'autres couleurs au besoin
    }

    return color_mapping.get(color_text_lower, discord.Color.default())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.command()
async def get_tempo_colors(ctx):
    url = 'https://www.kelwatt.fr/fournisseurs/edf/tempo'

    # Récupérer la page HTML
    response = requests.get(url)
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser la page HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Supposons que la couleur du jour est dans une balise avec la classe "current-day"
        current_day_color_element = soup.find('span', class_='text--xl badge badge--lg badge--neutral')
        tomorrow_color_element = soup.find('span', class_='text--xl badge badge--lg badge--word')

        # Extraire la couleur du jour
        if current_day_color_element and tomorrow_color_element:
            current_day_color_text = current_day_color_element.text.strip().lower()
            tomorrow_color_text = tomorrow_color_element.text.strip().lower()

            # Utiliser la fonction ou le dictionnaire pour obtenir la couleur Discord en fonction du texte
            current_day_discord_color = map_color_to_discord_color(current_day_color_text)
            tomorrow_discord_color = map_color_to_discord_color(tomorrow_color_text)
            
            # Obtenez la date actuelle
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
            tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y')

            # Afficher la couleur du jour dans le salon correspondant
            channel_day = client.get_channel(int(CHANNEL_ID_TEMPO))
            new_channel_name_day = f"Aujourd'hui - {current_day_color_text}"

            if channel_day:
                await channel_day.edit(name=new_channel_name_day)
            else:
                await ctx.send("Impossible de trouver le salon pour la couleur du jour avec l'ID spécifié.")

            # Afficher la couleur du lendemain dans le salon correspondant
            channel_tomorrow = client.get_channel(int(CHANNEL_ID_LEND))
            new_channel_name_tomorrow = f"Demain - {tomorrow_color_text}"

            if channel_tomorrow:
                await channel_tomorrow.edit(name=new_channel_name_tomorrow)
            else:
                await ctx.send("Impossible de trouver le salon pour la couleur du lendemain avec l'ID spécifié.")
            
            await ctx.send(f"La couleur Tempo du jour ({current_date}) est :", embed=discord.Embed(color=current_day_discord_color, description=f"**{current_day_color_text.upper()}**"))
            await ctx.send(f"La couleur Tempo du lendemain ({tomorrow_date}) est :", embed=discord.Embed(color=tomorrow_discord_color, description=f"**{tomorrow_color_text.upper()}**"))

            # Extraire le nombre de jours restants pour chaque couleur
            days_remaining_element = soup.find('td', colspan='2')
            if days_remaining_element:
                strong_elements = days_remaining_element.find_all('strong')
                if len(strong_elements) == 3:
                    days_info = {
                        'bleus': strong_elements[0].get_text(strip=True),
                        'blancs': strong_elements[1].get_text(strip=True),
                        'rouges': strong_elements[2].get_text(strip=True),
                    }
                    await ctx.send(f"Jours bleus restants : {days_info['bleus']}")
                    await ctx.send(f"Jours blancs restants : {days_info['blancs']}")
                    await ctx.send(f"Jours rouges restants : {days_info['rouges']}")
                else:
                    await ctx.send("Nombre incorrect de balises <strong> trouvées dans <td colspan='2'>.")
            else:
                await ctx.send("Balise <td colspan='2'> non trouvée.")
        else:
            await ctx.send("Impossible de trouver la couleur du jour ou du lendemain Tempo.")
    else:
        await ctx.send(f"La requête a échoué avec le code {response.status_code}.")

@client.command()
async def jour(ctx):
    await get_tempo_colors(ctx)  # Appeler la fonction existante pour obtenir les couleurs du jour et du lendemain

# Run the bot
client.run(TOKEN)
