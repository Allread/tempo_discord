# BOT DISCORD PYTHON - AFFICHAGE DES JOURS TEMPO

### How-to
Bot permettant l affichage de la couleur **TEMPO** du jour et celui du lendemain.
Il ajoute un message en embeds dans le salon où vous tapez la commande et édite le texte de 2 salons également.

Le bot ne demande que 2 autorisations particulières : GERER LES MESSAGES *(pour éditer ses messages)* et GERER LES SALONS *(pour éditer les noms des salons)*

### Comment ca marche ?
Le bot est soit manuel soit automatique. 
Vous pouvez lancer la demande des couleurs via la commande **!tempo** dans n'importe quel salon de votre serveur. Mais les messages iront dans le salon déclaré sous **CHANNEL_ID_ENVOI** dans config.py
A terme, le bot se lancera automatiquement à une heure définie par vous *(6h30 par défaut)*.

### Variables
Le code est documenté mais vous devez modifier les variables dans le fichier config.py :  

- Renommer le fichier **config.py.exemple** en **config.py**

- TOKEN = 'Le token du bot discord' ([*Token à créer ici*](https://discord.com/developers/applications "Token à créer ici"))
- CHANNEL_ID_TEMPO = 'id du salon J0 pour modifier le titre du salon'
- CHANNEL_ID_LEND = 'id du salon J+1 pour modifier le titre du salon'
- CHANNEL_ID_ENVOI = 'id du salon pour afficher les messages du bot'
- HEURE_LANCEMENT = 'heure à laquelle le bot se lance se mettre à jour'

Les IDs se trouve sur [votre client Discord en mode développeur](https://support.discord.com/hc/fr/articles/206346498-O%C3%B9-trouver-l-ID-de-mon-compte-utilisateur-serveur-message "votre client Discord en mode développeur")

### Images
![](https://github.com/Allread/tempo_discord/blob/main/screens/message_bot.png?raw=true)

![](https://github.com/Allread/tempo_discord/blob/main/screens/edit_salon.png?raw=true)


### A venir
- Lancement automatique à une heure précise
- 
