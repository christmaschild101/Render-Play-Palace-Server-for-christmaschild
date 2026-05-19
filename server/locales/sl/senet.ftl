# Lokalizacija Seneta

game-name-senet = Senet

# Začetek igre
senet-game-started = { $p1 } je igralec 1, { $p2 } je igralec 2. { $first } začne.

# Met paličic
senet-throw = { $player } vrže { $result }.{ $bonus ->
    [yes] {" "}Dodaten met!
   *[no] {""}
}

# Premikanje
senet-move-you = Premaknete se s polja { $from } na polje { $to }.
senet-move-other = { $player } se premakne s polja { $from } na polje { $to }.
senet-swap-you = Zamenjate se z { $opponent } na polju { $to }. { $opponent } se vrne na polje { $from }.
senet-swap-other = { $player } se zamenja z { $opponent } na polju { $to }. { $opponent } se vrne na polje { $from }.
senet-bearoff-you = Iznesete figuro s polja { $from }. Ostane { $remaining }.
senet-bearoff-other = { $player } iznese figuro s polja { $from }. Ostane { $remaining }.
senet-water-you = Pristali ste v Hiši vode! Figura poslana na polje { $dest }.
senet-water-other = { $player } je pristal v Hiši vode! Figura poslana na polje { $dest }.
senet-happiness-you = Dosegli ste Hišo sreče.
senet-happiness-other = { $player } je dosegel Hišo sreče.

# Ni potez
senet-no-moves-you = Nimate nobenega dovoljenega poteza.
senet-no-moves-other = { $player } nima nobenega dovoljenega poteza.

# Opisi polj
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, vaše
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, vaše
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Imena posebnih polj
senet-house-rebirth = Preporod
senet-house-happiness = Sreča
senet-house-water = Voda
senet-house-three-truths = Tri resnice
senet-house-re-atum = Re-Atum

# Stanje igre
senet-status = { $p1 }: { $off1 } iznešenih. { $p2 }: { $off2 } iznešenih.{ $phase ->
    [throwing] {" "}Čakanje na met.
   *[moving] {" "}Met: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Še ni meta.

# Zmaga
senet-wins = { $player } zmaga! Vse figure so iznešene.

# Oznake dejanj
senet-check-status = Stanje
senet-check-sticks = Paličice
senet-check-score = Rezultat
senet-score = { $p1 }: { $off1 } iznešenih. { $p2 }: { $off2 } iznešenih.

# Napake
senet-not-your-piece = To ni vaša figura.
senet-no-piece-there = Na tem polju ni figure.
senet-no-moves-from-here = S tega polja ni dovoljenih potez.

# Možnosti
senet-option-bot-difficulty = Težavnost bota: { $bot_difficulty }
senet-option-select-bot-difficulty = Izberite težavnost bota
senet-option-changed-bot-difficulty = Težavnost bota nastavljena na { $bot_difficulty }.
senet-difficulty-random = Naključno
senet-difficulty-simple = Preprosto
