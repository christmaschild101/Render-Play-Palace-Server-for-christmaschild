# Lokalizace Senetu

game-name-senet = Senet

# Zahájení hry
senet-game-started = { $p1 } je hráč 1, { $p2 } je hráč 2. { $first } začíná.

# Hod tyčkami
senet-throw = { $player } hodí { $result }.{ $bonus ->
    [yes] {" "}Bonusový hod!
   *[no] {""}
}

# Pohyb
senet-move-you = Přesunete se z pole { $from } na pole { $to }.
senet-move-other = { $player } se přesune z pole { $from } na pole { $to }.
senet-swap-you = Vyměníte se s { $opponent } na poli { $to }. { $opponent } se vrátí na pole { $from }.
senet-swap-other = { $player } se vymění s { $opponent } na poli { $to }. { $opponent } se vrátí na pole { $from }.
senet-bearoff-you = Vynesete figurku z pole { $from }. Zbývá { $remaining }.
senet-bearoff-other = { $player } vynese figurku z pole { $from }. Zbývá { $remaining }.
senet-water-you = Přistáli jste v Domě vody! Figurka odeslána na pole { $dest }.
senet-water-other = { $player } přistál v Domě vody! Figurka odeslána na pole { $dest }.
senet-happiness-you = Dosáhli jste Domu štěstí.
senet-happiness-other = { $player } dosáhl Domu štěstí.

# Žádné tahy
senet-no-moves-you = Nemáte žádné platné tahy.
senet-no-moves-other = { $player } nemá žádné platné tahy.

# Popis polí
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, vaše
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, vaše
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Názvy speciálních polí
senet-house-rebirth = Znovuzrození
senet-house-happiness = Štěstí
senet-house-water = Voda
senet-house-three-truths = Tři pravdy
senet-house-re-atum = Re-Atum

# Stav hry
senet-status = { $p1 }: { $off1 } vyneseno. { $p2 }: { $off2 } vyneseno.{ $phase ->
    [throwing] {" "}Čeká se na hod.
   *[moving] {" "}Hod: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Zatím žádný hod.

# Výhra
senet-wins = { $player } vyhrál! Všechny figurky jsou vyneseny.

# Popisky akcí
senet-check-status = Stav
senet-check-sticks = Tyčky
senet-check-score = Skóre
senet-score = { $p1 }: { $off1 } vyneseno. { $p2 }: { $off2 } vyneseno.

# Chyby
senet-not-your-piece = To není vaše figurka.
senet-no-piece-there = Na tomto poli není žádná figurka.
senet-no-moves-from-here = Z tohoto pole nejsou žádné platné tahy.

# Možnosti
senet-option-bot-difficulty = Obtížnost bota: { $bot_difficulty }
senet-option-select-bot-difficulty = Vyberte obtížnost bota
senet-option-changed-bot-difficulty = Obtížnost bota nastavena na { $bot_difficulty }.
senet-difficulty-random = Náhodný
senet-difficulty-simple = Jednoduchý
