# Localisation de Senet

game-name-senet = Senet

# Début de partie
senet-game-started = { $p1 } est le joueur 1, { $p2 } est le joueur 2. { $first } commence.

# Lancer de bâtons
senet-throw = { $player } lance { $result }.{ $bonus ->
    [yes] {" "}Tour supplémentaire !
   *[no] {""}
}

# Déplacement
senet-move-you = Vous déplacez de la case { $from } à la case { $to }.
senet-move-other = { $player } se déplace de la case { $from } à la case { $to }.
senet-swap-you = Vous échangez avec { $opponent } sur la case { $to }. { $opponent } retourne à la case { $from }.
senet-swap-other = { $player } échange avec { $opponent } sur la case { $to }. { $opponent } retourne à la case { $from }.
senet-bearoff-you = Vous sortez du plateau depuis la case { $from }. Il en reste { $remaining }.
senet-bearoff-other = { $player } sort du plateau depuis la case { $from }. Il en reste { $remaining }.
senet-water-you = Vous êtes tombé dans la Maison de l'Eau ! Pièce envoyée à la case { $dest }.
senet-water-other = { $player } est tombé dans la Maison de l'Eau ! Pièce envoyée à la case { $dest }.
senet-happiness-you = Vous avez atteint la Maison du Bonheur.
senet-happiness-other = { $player } a atteint la Maison du Bonheur.

# Aucun mouvement
senet-no-moves-you = Vous n'avez aucun mouvement légal.
senet-no-moves-other = { $player } n'a aucun mouvement légal.

# Étiquettes des cases
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, à vous
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, à vous
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Noms des cases spéciales
senet-house-rebirth = Renaissance
senet-house-happiness = Bonheur
senet-house-water = Eau
senet-house-three-truths = Trois Vérités
senet-house-re-atum = Ré-Atoum

# Statut
senet-status = { $p1 } : { $off1 } sorties. { $p2 } : { $off2 } sorties.{ $phase ->
    [throwing] {" "}En attente du lancer.
   *[moving] {" "}Résultat : { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Aucun lancer pour l'instant.

# Victoire
senet-wins = { $player } gagne ! Toutes les pièces sont sorties du plateau.

# Étiquettes des actions
senet-check-status = Statut
senet-check-sticks = Bâtons
senet-check-score = Score
senet-score = { $p1 } : { $off1 } sorties. { $p2 } : { $off2 } sorties.

# Erreurs
senet-not-your-piece = Ce n'est pas votre pièce.
senet-no-piece-there = Il n'y a aucune pièce ici.
senet-no-moves-from-here = Aucun mouvement légal depuis cette case.

# Options
senet-option-bot-difficulty = Difficulté du bot : { $bot_difficulty }
senet-option-select-bot-difficulty = Choisir la difficulté du bot
senet-option-changed-bot-difficulty = Difficulté du bot réglée sur { $bot_difficulty }.
senet-difficulty-random = Aléatoire
senet-difficulty-simple = Simple
