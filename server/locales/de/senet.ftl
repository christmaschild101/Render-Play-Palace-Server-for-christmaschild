# Senet-Lokalisierung

game-name-senet = Senet

# Spielbeginn
senet-game-started = { $p1 } ist Spieler 1, { $p2 } ist Spieler 2. { $first } beginnt.

# Wurfstäbe
senet-throw = { $player } wirft { $result }.{ $bonus ->
    [yes] {" "}Bonuswurf!
   *[no] {""}
}

# Bewegung
senet-move-you = Sie ziehen von Feld { $from } auf Feld { $to }.
senet-move-other = { $player } zieht von Feld { $from } auf Feld { $to }.
senet-swap-you = Sie tauschen mit { $opponent } auf Feld { $to }. { $opponent } geht zurück auf Feld { $from }.
senet-swap-other = { $player } tauscht mit { $opponent } auf Feld { $to }. { $opponent } geht zurück auf Feld { $from }.
senet-bearoff-you = Sie tragen ab von Feld { $from }. Noch { $remaining } übrig.
senet-bearoff-other = { $player } trägt ab von Feld { $from }. Noch { $remaining } übrig.
senet-water-you = Sie landen im Haus des Wassers! Spielstein auf Feld { $dest } gesetzt.
senet-water-other = { $player } landet im Haus des Wassers! Spielstein auf Feld { $dest } gesetzt.
senet-happiness-you = Sie haben das Haus der Freude erreicht.
senet-happiness-other = { $player } hat das Haus der Freude erreicht.

# Keine Züge
senet-no-moves-you = Sie haben keine gültigen Züge.
senet-no-moves-other = { $player } hat keine gültigen Züge.

# Feldbeschriftungen
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, Ihres
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, Ihres
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Sonderfeld-Namen
senet-house-rebirth = Wiedergeburt
senet-house-happiness = Freude
senet-house-water = Wasser
senet-house-three-truths = Drei Wahrheiten
senet-house-re-atum = Re-Atum

# Status
senet-status = { $p1 }: { $off1 } abgetragen. { $p2 }: { $off2 } abgetragen.{ $phase ->
    [throwing] {" "}Warten auf Wurf.
   *[moving] {" "}Wurf: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Noch kein Wurf.

# Sieg
senet-wins = { $player } gewinnt! Alle Spielsteine abgetragen.

# Aktionsbezeichnungen
senet-check-status = Status
senet-check-sticks = Stäbe
senet-check-score = Punkte
senet-score = { $p1 }: { $off1 } abgetragen. { $p2 }: { $off2 } abgetragen.

# Fehler
senet-not-your-piece = Das ist nicht Ihr Spielstein.
senet-no-piece-there = Kein Spielstein dort.
senet-no-moves-from-here = Keine gültigen Züge von diesem Feld.

# Optionen
senet-option-bot-difficulty = Bot-Schwierigkeit: { $bot_difficulty }
senet-option-select-bot-difficulty = Bot-Schwierigkeit auswählen
senet-option-changed-bot-difficulty = Bot-Schwierigkeit auf { $bot_difficulty } gesetzt.
senet-difficulty-random = Zufällig
senet-difficulty-simple = Einfach
