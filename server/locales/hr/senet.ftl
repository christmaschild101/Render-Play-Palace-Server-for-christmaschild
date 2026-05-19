# Lokalizacija Seneta

game-name-senet = Senet

# Početak igre
senet-game-started = { $p1 } je igrač 1, { $p2 } je igrač 2. { $first } ide prvi.

# Bacanje štapića
senet-throw = { $player } baca { $result }.{ $bonus ->
    [yes] {" "}Dodatno bacanje!
   *[no] {""}
}

# Kretanje
senet-move-you = Premještate se s polja { $from } na polje { $to }.
senet-move-other = { $player } se premješta s polja { $from } na polje { $to }.
senet-swap-you = Mijenjate se s { $opponent } na polju { $to }. { $opponent } se vraća na polje { $from }.
senet-swap-other = { $player } se mijenja s { $opponent } na polju { $to }. { $opponent } se vraća na polje { $from }.
senet-bearoff-you = Izvodite figuru s polja { $from }. Preostalo { $remaining }.
senet-bearoff-other = { $player } izvodi figuru s polja { $from }. Preostalo { $remaining }.
senet-water-you = Sletjeli ste u Kuću vode! Figura poslana na polje { $dest }.
senet-water-other = { $player } je sletio u Kuću vode! Figura poslana na polje { $dest }.
senet-happiness-you = Stigli ste do Kuće sreće.
senet-happiness-other = { $player } je stigao do Kuće sreće.

# Nema poteza
senet-no-moves-you = Nemate nijedan dopušten potez.
senet-no-moves-other = { $player } nema nijedan dopušten potez.

# Opisi polja
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, vaše
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, vaše
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nazivi posebnih polja
senet-house-rebirth = Preporod
senet-house-happiness = Sreća
senet-house-water = Voda
senet-house-three-truths = Tri istine
senet-house-re-atum = Re-Atum

# Status igre
senet-status = { $p1 }: { $off1 } izvedenih. { $p2 }: { $off2 } izvedenih.{ $phase ->
    [throwing] {" "}Čeka se bacanje.
   *[moving] {" "}Bacanje: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Još nema bacanja.

# Pobjeda
senet-wins = { $player } pobjeđuje! Sve figure su izvedene.

# Oznake radnji
senet-check-status = Status
senet-check-sticks = Štapići
senet-check-score = Rezultat
senet-score = { $p1 }: { $off1 } izvedenih. { $p2 }: { $off2 } izvedenih.

# Greške
senet-not-your-piece = To nije vaša figura.
senet-no-piece-there = Na tom polju nema figure.
senet-no-moves-from-here = S ovog polja nema dopuštenih poteza.

# Mogućnosti
senet-option-bot-difficulty = Težina bota: { $bot_difficulty }
senet-option-select-bot-difficulty = Odaberite težinu bota
senet-option-changed-bot-difficulty = Težina bota postavljena na { $bot_difficulty }.
senet-difficulty-random = Nasumično
senet-difficulty-simple = Jednostavno
