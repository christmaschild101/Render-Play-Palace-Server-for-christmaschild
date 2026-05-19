# Localizzazione di Senet

game-name-senet = Senet

# Inizio partita
senet-game-started = { $p1 } è il giocatore 1, { $p2 } è il giocatore 2. { $first } inizia.

# Lancio dei bastoni
senet-throw = { $player } lancia { $result }.{ $bonus ->
    [yes] {" "}Turno extra!
   *[no] {""}
}

# Movimento
senet-move-you = Sposti dalla casella { $from } alla casella { $to }.
senet-move-other = { $player } sposta dalla casella { $from } alla casella { $to }.
senet-swap-you = Scambi con { $opponent } sulla casella { $to }. { $opponent } torna alla casella { $from }.
senet-swap-other = { $player } scambia con { $opponent } sulla casella { $to }. { $opponent } torna alla casella { $from }.
senet-bearoff-you = Esci dal tabellone dalla casella { $from }. Ne rimangono { $remaining }.
senet-bearoff-other = { $player } esce dal tabellone dalla casella { $from }. Ne rimangono { $remaining }.
senet-water-you = Sei caduto nella Casa dell'Acqua! Pedina inviata alla casella { $dest }.
senet-water-other = { $player } è caduto nella Casa dell'Acqua! Pedina inviata alla casella { $dest }.
senet-happiness-you = Hai raggiunto la Casa della Felicità.
senet-happiness-other = { $player } ha raggiunto la Casa della Felicità.

# Nessuna mossa
senet-no-moves-you = Non hai mosse legali disponibili.
senet-no-moves-other = { $player } non ha mosse legali disponibili.

# Etichette delle caselle
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, tua
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, tua
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nomi delle caselle speciali
senet-house-rebirth = Rinascita
senet-house-happiness = Felicità
senet-house-water = Acqua
senet-house-three-truths = Tre Verità
senet-house-re-atum = Ra-Atum

# Stato
senet-status = { $p1 }: { $off1 } uscite. { $p2 }: { $off2 } uscite.{ $phase ->
    [throwing] {" "}In attesa del lancio.
   *[moving] {" "}Lancio: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Nessun lancio ancora.

# Vittoria
senet-wins = { $player } vince! Tutte le pedine sono uscite dal tabellone.

# Etichette delle azioni
senet-check-status = Stato
senet-check-sticks = Bastoni
senet-check-score = Punteggio
senet-score = { $p1 }: { $off1 } uscite. { $p2 }: { $off2 } uscite.

# Errori
senet-not-your-piece = Quella non è la tua pedina.
senet-no-piece-there = Non c'è nessuna pedina qui.
senet-no-moves-from-here = Nessuna mossa legale da questa casella.

# Opzioni
senet-option-bot-difficulty = Difficoltà del bot: { $bot_difficulty }
senet-option-select-bot-difficulty = Seleziona la difficoltà del bot
senet-option-changed-bot-difficulty = Difficoltà del bot impostata su { $bot_difficulty }.
senet-difficulty-random = Casuale
senet-difficulty-simple = Semplice
