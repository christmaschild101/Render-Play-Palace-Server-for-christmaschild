# Localizarea Senet

game-name-senet = Senet

# Începutul jocului
senet-game-started = { $p1 } este jucătorul 1, { $p2 } este jucătorul 2. { $first } începe primul.

# Aruncarea bețelor
senet-throw = { $player } aruncă { $result }.{ $bonus ->
    [yes] {" "}Aruncare bonus!
   *[no] {""}
}

# Mișcare
senet-move-you = Te muți de pe pătratul { $from } pe pătratul { $to }.
senet-move-other = { $player } se mută de pe pătratul { $from } pe pătratul { $to }.
senet-swap-you = Schimbi locul cu { $opponent } pe pătratul { $to }. { $opponent } se întoarce pe pătratul { $from }.
senet-swap-other = { $player } schimbă locul cu { $opponent } pe pătratul { $to }. { $opponent } se întoarce pe pătratul { $from }.
senet-bearoff-you = Ieși de pe tablă de pe pătratul { $from }. Mai rămân { $remaining }.
senet-bearoff-other = { $player } iese de pe tablă de pe pătratul { $from }. Mai rămân { $remaining }.
senet-water-you = Ai căzut în Casa Apei! Piesa trimisă pe pătratul { $dest }.
senet-water-other = { $player } a căzut în Casa Apei! Piesa trimisă pe pătratul { $dest }.
senet-happiness-you = Ai ajuns la Casa Fericirii.
senet-happiness-other = { $player } a ajuns la Casa Fericirii.

# Fără mutări
senet-no-moves-you = Nu ai mutări legale disponibile.
senet-no-moves-other = { $player } nu are mutări legale disponibile.

# Etichete pătrate
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, a ta
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, a ta
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Numele pătratelor speciale
senet-house-rebirth = Renaștere
senet-house-happiness = Fericire
senet-house-water = Apă
senet-house-three-truths = Cele Trei Adevăruri
senet-house-re-atum = Ra-Atum

# Stare
senet-status = { $p1 }: { $off1 } ieșite. { $p2 }: { $off2 } ieșite.{ $phase ->
    [throwing] {" "}Se așteaptă aruncarea.
   *[moving] {" "}Aruncare: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Nicio aruncare încă.

# Victorie
senet-wins = { $player } câștigă! Toate piesele au ieșit de pe tablă.

# Etichete acțiuni
senet-check-status = Stare
senet-check-sticks = Bețe
senet-check-score = Scor
senet-score = { $p1 }: { $off1 } ieșite. { $p2 }: { $off2 } ieșite.

# Erori
senet-not-your-piece = Aceasta nu este piesa ta.
senet-no-piece-there = Nu există nicio piesă acolo.
senet-no-moves-from-here = Nicio mutare legală de pe acest pătrat.

# Opțiuni
senet-option-bot-difficulty = Dificultatea botului: { $bot_difficulty }
senet-option-select-bot-difficulty = Selectează dificultatea botului
senet-option-changed-bot-difficulty = Dificultatea botului setată la { $bot_difficulty }.
senet-difficulty-random = Aleatoriu
senet-difficulty-simple = Simplu
