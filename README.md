# BOT DISCORD PYTHON - AFFICHAGE DES JOURS TEMPO

### How-to
Bot permettant l affichage de la couleur **TEMPO** du jour et celui du lendemain.
Il ajoute un message en embeds dans le salon où vous tapez la commande et édite le texte de 2 salons également.

Le bot ne demande que 2 autorisations particulières : GERER LES MESSAGES *(pour éditer ses messages)* et GERER LES SALONS *(pour éditer les noms des salons)*

### Variables

Le code est documenté mais vous devez modifier 3 variables dans le fichier config.py :  

- Renommer le fichier **config.py.exemple** en **config.py**

- TOKEN = 'Le token du bot discord' ([*Token à créer ici*](https://discord.com/developers/applications "Token à créer ici"))
- CHANNEL_ID_TEMPO = 'id du salon J0 pour modifier le titre du salon'
- CHANNEL_ID_LEND = 'id du salon J+1 pour modifier le titre du salon'
- CHANNEL_ID_ENVOI = 'id du salon pour récuperer les envoi des jours'
- HEURE_LANCEMENT = 'l'heure à laquelle le bot se lance se mettre à jour'

Les IDs se trouve sur [votre client Discord en mode développeur](https://support.discord.com/hc/fr/articles/206346498-O%C3%B9-trouver-l-ID-de-mon-compte-utilisateur-serveur-message "votre client Discord en mode développeur")

### Images
![](https://github.com/Allread/tempo_discord/blob/main/screens/screen3.png?raw=true)

![](https://github.com/Allread/tempo_discord/blob/main/screens/edit_salon.png?raw=true)


### A venir
- Lancement automatique à une heure précise
- Ajout des jours restants TEMPO par couleur
- 
