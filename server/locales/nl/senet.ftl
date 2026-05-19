# Senet-lokalisatie

game-name-senet = Senet

# Spelstart
senet-game-started = { $p1 } is speler 1, { $p2 } is speler 2. { $first } begint.

# Werpstokjes
senet-throw = { $player } gooit { $result }.{ $bonus ->
    [yes] {" "}Bonusworp!
   *[no] {""}
}

# Beweging
senet-move-you = U beweegt van vak { $from } naar vak { $to }.
senet-move-other = { $player } beweegt van vak { $from } naar vak { $to }.
senet-swap-you = U wisselt met { $opponent } op vak { $to }. { $opponent } gaat terug naar vak { $from }.
senet-swap-other = { $player } wisselt met { $opponent } op vak { $to }. { $opponent } gaat terug naar vak { $from }.
senet-bearoff-you = U draagt af van vak { $from }. Nog { $remaining } over.
senet-bearoff-other = { $player } draagt af van vak { $from }. Nog { $remaining } over.
senet-water-you = U belandt in het Huis van het Water! Stuk naar vak { $dest } gestuurd.
senet-water-other = { $player } belandt in het Huis van het Water! Stuk naar vak { $dest } gestuurd.
senet-happiness-you = U heeft het Huis van Geluk bereikt.
senet-happiness-other = { $player } heeft het Huis van Geluk bereikt.

# Geen zetten
senet-no-moves-you = U heeft geen geldige zetten.
senet-no-moves-other = { $player } heeft geen geldige zetten.

# Vakbeschrijvingen
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, van u
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, van u
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Namen van speciale vakken
senet-house-rebirth = Wedergeboorte
senet-house-happiness = Geluk
senet-house-water = Water
senet-house-three-truths = Drie Waarheden
senet-house-re-atum = Re-Atum

# Status
senet-status = { $p1 }: { $off1 } af. { $p2 }: { $off2 } af.{ $phase ->
    [throwing] {" "}Wachten op worp.
   *[moving] {" "}Worp: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Nog niet gegooid.

# Winst
senet-wins = { $player } wint! Alle stukken afgedragen.

# Actielabels
senet-check-status = Status
senet-check-sticks = Stokjes
senet-check-score = Score
senet-score = { $p1 }: { $off1 } af. { $p2 }: { $off2 } af.

# Fouten
senet-not-your-piece = Dat is niet uw stuk.
senet-no-piece-there = Geen stuk op dat vak.
senet-no-moves-from-here = Geen geldige zetten vanaf dit vak.

# Opties
senet-option-bot-difficulty = Botmoeilijkheid: { $bot_difficulty }
senet-option-select-bot-difficulty = Selecteer botmoeilijkheid
senet-option-changed-bot-difficulty = Botmoeilijkheid ingesteld op { $bot_difficulty }.
senet-difficulty-random = Willekeurig
senet-difficulty-simple = Eenvoudig
