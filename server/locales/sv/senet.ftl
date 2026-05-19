# Senet-lokalisering

game-name-senet = Senet

# Spelstart
senet-game-started = { $p1 } är spelare 1, { $p2 } är spelare 2. { $first } börjar.

# Kaststickor
senet-throw = { $player } kastar { $result }.{ $bonus ->
    [yes] {" "}Bonuskast!
   *[no] {""}
}

# Förflyttning
senet-move-you = Du flyttar från ruta { $from } till ruta { $to }.
senet-move-other = { $player } flyttar från ruta { $from } till ruta { $to }.
senet-swap-you = Du byter plats med { $opponent } på ruta { $to }. { $opponent } går tillbaka till ruta { $from }.
senet-swap-other = { $player } byter plats med { $opponent } på ruta { $to }. { $opponent } går tillbaka till ruta { $from }.
senet-bearoff-you = Du bär av från ruta { $from }. { $remaining } kvar.
senet-bearoff-other = { $player } bär av från ruta { $from }. { $remaining } kvar.
senet-water-you = Du landade i Vattnets hus! Pjäs skickad till ruta { $dest }.
senet-water-other = { $player } landade i Vattnets hus! Pjäs skickad till ruta { $dest }.
senet-happiness-you = Du har nått Lycksalighetens hus.
senet-happiness-other = { $player } har nått Lycksalighetens hus.

# Inga drag
senet-no-moves-you = Du har inga giltiga drag.
senet-no-moves-other = { $player } har inga giltiga drag.

# Rutabeskrivningar
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, din
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, din
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Namn på specialrutor
senet-house-rebirth = Återfödelse
senet-house-happiness = Lycksalighet
senet-house-water = Vatten
senet-house-three-truths = Tre Sanningar
senet-house-re-atum = Re-Atum

# Status
senet-status = { $p1 }: { $off1 } avbärda. { $p2 }: { $off2 } avbärda.{ $phase ->
    [throwing] {" "}Väntar på kast.
   *[moving] {" "}Kast: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Inget kast ännu.

# Vinst
senet-wins = { $player } vinner! Alla pjäser avbärda.

# Handlingsetiketter
senet-check-status = Status
senet-check-sticks = Stickor
senet-check-score = Poäng
senet-score = { $p1 }: { $off1 } avbärda. { $p2 }: { $off2 } avbärda.

# Fel
senet-not-your-piece = Det är inte din pjäs.
senet-no-piece-there = Ingen pjäs där.
senet-no-moves-from-here = Inga giltiga drag från den här rutan.

# Alternativ
senet-option-bot-difficulty = Botsvårighetsgrad: { $bot_difficulty }
senet-option-select-bot-difficulty = Välj botsvårighetsgrad
senet-option-changed-bot-difficulty = Botsvårighetsgrad inställd på { $bot_difficulty }.
senet-difficulty-random = Slumpmässig
senet-difficulty-simple = Enkel
